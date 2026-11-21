#!/usr/bin/env python3
"""Small synchronous client for OpenCode Go's Chat Completions API."""

import json
import http.client
import os
import re
import threading
import time
from contextvars import ContextVar
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener
from uuid import uuid4

ENDPOINT = "https://opencode.ai/inference/go/openai/v1/chat/completions"
MODELS = {
    "deepseekflash1017": "deepseek-v4.1-flash",
    "deepseek-v4.1-flash": "deepseek-v4.1-flash",
    "Gemini 4 Hydrogen": "gemini-4-hydrogen",
    "gemini-4-hydrogen": "gemini-4-hydrogen",
    "beam-free": "beam-free",
    "gpt-6-luna": "gpt-6-luna",
    "hy4": "hy4",
    "hy4-flash-free": "hy4-flash-free",
}
LOG = Path(__file__).resolve().parent / "output" / "llm_calls.jsonl"
LOG_PATH = ContextVar("llm_log_path", default=None)
REASONING_EFFORT = ContextVar("llm_reasoning_effort", default=None)
THINKING = ContextVar("llm_thinking", default=None)
TRANSPORT = ContextVar("llm_transport_policy", default=None)
MIN_INTERVAL_SECONDS = 1.0
MAX_ATTEMPTS = 3
MAX_RETRY_WAIT_SECONDS = 90
_rate_lock = threading.Lock()
_log_lock = threading.Lock()
_next_request = 0.0


class LLMError(RuntimeError):
    pass


class RefuseRedirects(HTTPRedirectHandler):
    # Attach the bearer token only to the documented endpoint.
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = build_opener(RefuseRedirects())


def api_key():
    for name in ("OPENCODE_GO_API_KEY", "OPENCODE_API_KEY"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    data_dir = Path(os.environ.get("XDG_DATA_HOME") or Path.home() / ".local/share")
    try:
        records = json.loads((data_dir / "opencode/auth.json").read_text())
        provider = records["opencode-go"]
        if provider.get("type") == "api":
            key = provider.get("key")
            if isinstance(key, str) and key.strip():
                return key.strip()
    except (OSError, ValueError, TypeError, AttributeError, KeyError):
        pass
    return ""


def redact(value, key):
    if isinstance(value, str):
        if key:
            value = value.replace(key, "[REDACTED]")
        return re.sub(r"\bBearer\s+[^\s,;\x22]+", "Bearer [REDACTED]", value,
                      flags=re.IGNORECASE)
    if isinstance(value, dict):
        return {name: redact(item, key) for name, item in value.items()}
    return value


def write_log(record, key):
    with _log_lock:
        target = LOG_PATH.get() or LOG
        target.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        with os.fdopen(fd, "a", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), 0o600)
            record = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), **record}
            stream.write(json.dumps(redact(record, key), ensure_ascii=False) + "\n")


def wait_for_slot(delay=0):
    global _next_request
    with _rate_lock:
        _next_request = max(_next_request, time.monotonic() + delay)
    while True:
        with _rate_lock:
            now = time.monotonic()
            wait = _next_request - now
            if wait <= 0:
                _next_request = now + MIN_INTERVAL_SECONDS
                return
        time.sleep(wait)


def retry_after_seconds(value):
    if value is None:
        return 0
    try:
        return max(0, int(value))
    except ValueError:
        try:
            date = parsedate_to_datetime(value)
            return max(0, date.timestamp() - time.time())
        except (TypeError, ValueError, OverflowError):
            return 0


def read_stream(response):
    pieces, usage = [], {}
    model, finish = None, None
    for line in response:
        if not line.startswith(b"data:"):
            continue
        payload = line[5:].strip()
        if payload == b"[DONE]":
            break
        event = json.loads(payload)
        model = event.get("model") or model
        usage = event.get("usage") or usage
        choices = event.get("choices") or []
        if choices:
            choice = choices[0]
            text = choice.get("delta", {}).get("content")
            if text:
                pieces.append(text)
            finish = choice.get("finish_reason") or finish
    if not model or not finish:
        raise OSError("Completion stream ended before its final event")
    return {"model": model, "usage": usage,
            "choices": [{"message": {"content": "".join(pieces)}, "finish_reason": finish}]}


def call_llm(model, prompt, temperature, max_tokens):
    """Return content, reported model, finish reason, usage and timing for one Go call."""
    model_id = MODELS.get(model)
    if model_id is None:
        raise ValueError("Use a configured OpenCode Go model ID")
    started = time.monotonic()
    key = api_key()
    session = "ses_" + uuid4().hex
    base = {"model_requested": model_id, "endpoint": ENDPOINT, "session": session,
            "prompt": prompt, "temperature": temperature, "max_tokens": max_tokens}
    effort = REASONING_EFFORT.get()
    thinking = THINKING.get()
    policy = TRANSPORT.get() or {}
    stream = policy.get("stream", True)
    timeout = policy.get("timeout_seconds", 220)
    attempts = policy.get("max_attempts", MAX_ATTEMPTS)
    max_wait = policy.get("max_retry_wait_seconds", MAX_RETRY_WAIT_SECONDS)
    if effort:
        base["reasoning_effort"] = effort
    if thinking:
        base["thinking"] = thinking
    base["stream"] = stream
    base["timeout_seconds"] = timeout
    if not key:
        write_log({**base, "attempt": 0, "status": "missing_credentials", "response": None}, key)
        raise LLMError("Set OPENCODE_GO_API_KEY or OPENCODE_API_KEY, or connect OpenCode Go.")

    body = {
        "model": model_id, "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature, "max_tokens": max_tokens, "stream": stream,
    }
    if stream:
        body["stream_options"] = {"include_usage": True}
    if effort:
        body["reasoning_effort"] = effort
    if thinking:
        body["thinking"] = {"type": thinking}
    payload = json.dumps(body).encode()
    request = Request(ENDPOINT, data=payload, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "User-Agent": "autobench-preflight/1.0", "x-opencode-session": session,
    })
    delay = 0
    for attempt in range(1, attempts + 1):
        wait_for_slot(delay)
        attempt_started = time.monotonic()
        record = {**base, "attempt": attempt, "is_retry": attempt > 1, "truncated": False}
        status = None
        rate_headers = {}
        provider_error = {}
        retry_after = 0
        try:
            with _opener.open(request, timeout=timeout) as response:
                status = response.status
                rate_headers = rate_limit_headers(response.headers)
                result = read_stream(response) if stream else json.load(response)
            choice = result["choices"][0]
            content = choice["message"].get("content")
            actual_model = result["model"]
            if not isinstance(actual_model, str) or not actual_model:
                raise ValueError("Missing API model ID")
            finish = choice.get("finish_reason")
            usage = result.get("usage") or {}
            if not isinstance(usage, dict):
                raise ValueError("Invalid usage object")
        except HTTPError as exc:
            status = exc.code
            rate_headers = rate_limit_headers(exc.headers)
            retry_after = retry_after_seconds(exc.headers.get("Retry-After"))
            try:
                body = json.loads(exc.read(8192))
                details = body.get("error", {})
                if isinstance(details, dict):
                    provider_error = {
                        field: redact(details[field], key)[:400]
                        for field in ("type", "code", "message") if isinstance(details.get(field), str)
                    }
                elif isinstance(details, str):
                    provider_error = {"message": redact(details, key)[:400]}
            except (AttributeError, OSError, ValueError):
                pass
            finally:
                exc.close()
            error = f"HTTP {status}"
            transient = status in (408, 429) or 500 <= status <= 599
        except (URLError, OSError, http.client.HTTPException) as exc:
            error = type(exc).__name__
            transient = True
        except (AttributeError, IndexError, KeyError, TypeError, ValueError):
            error = "invalid_response"
            transient = False
        else:
            metadata = usage.get("opencode") or result.get("opencode")
            allowance = metadata.get("allowance") if isinstance(metadata, dict) else None
            billing_source = metadata.get("billing_source") if isinstance(metadata, dict) else None
            charged = usage.get("cost")
            list_cost = metadata.get("list_cost") if isinstance(metadata, dict) else None
            answer = {
                "model_requested": model_id, "model_actual": actual_model.replace(key, "[REDACTED]"),
                "attempt": attempt, "http_status": status, "status": "received",
                "finish_reason": finish.replace(key, "[REDACTED]") if isinstance(finish, str) else None,
                "truncated": finish == "length",
                "response": content,
                "complete": finish == "stop" and isinstance(content, str) and bool(content.strip()),
                "request_seconds": round(time.monotonic() - attempt_started, 3),
                "elapsed_seconds": round(time.monotonic() - started, 3),
                "allowance": allowance if type(allowance) in (int, float) else None,
                "charged_usd": charged if type(charged) in (int, float) else None,
                "list_cost_usd": list_cost if type(list_cost) in (int, float) else None,
                "billing_source": billing_source if billing_source in
                ("free", "balance", "go", "go-plus", "go-teams", "byok") else None,
                "rate_limit_headers": redact(rate_headers, key),
                "usage": {k: v for k, v in usage.items()
                          if isinstance(v, int) and k in
                          ("prompt_tokens", "completion_tokens", "total_tokens")},
            }
            retry_length = (answer["truncated"] and policy.get("retry_truncation") and
                            attempt < attempts)
            write_log({**record, **answer, "will_retry": bool(retry_length)}, key)
            if retry_length:
                delay = 2 ** (attempt - 1)
                continue
            return answer

        delay = max(2 ** (attempt - 1), retry_after)
        retry = transient and attempt < attempts and delay <= max_wait
        write_log({**record, "status": error, "http_status": status, "response": None,
                   "provider_error": provider_error, "rate_limit_headers": rate_headers,
                   "will_retry": bool(retry),
                   "request_seconds": round(time.monotonic() - attempt_started, 3),
                   "retry_in_seconds": delay if retry else None}, key)
        if not retry:
            detail = provider_error.get("message") or provider_error.get("code") or ""
            raise LLMError(f"{model_id} Go request failed ({error})" +
                           (f" — {detail}" if detail else ""))


def rate_limit_headers(headers):
    return {name.lower(): value for name, value in headers.items()
            if name.lower().startswith(("x-ratelimit-", "ratelimit-"))}


def main():
    prompt = "Write a complete Verilog module for a 2-to-1, 1-bit multiplexer. Return only Verilog."
    exit_code = 0
    for model in ("deepseekflash1017", "gemini-4-hydrogen"):
        try:
            result = call_llm(model, prompt, temperature=0, max_tokens=512)
        except LLMError as exc:
            print(f"{model} — {exc}")
            exit_code = 1
            continue
        content = result.pop("response")
        module_complete = result["complete"] and bool(
            re.search(r"\bmodule\b.+\bendmodule\b", content, re.DOTALL)
        )
        print(json.dumps({**result, "complete_verilog": module_complete}, ensure_ascii=False))
        if not module_complete:
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
