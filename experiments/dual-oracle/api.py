"""Check-pointed native-thinking requests using the locked v3 transport."""

import ast
import contextvars
import json
import os
import re
import subprocess
import threading
import tokenize
from io import StringIO

from data import PLAN, atomic, load, save, setup
import llm

llm.api_key = lambda: os.environ.get("OPENCODE_GO_API_KEY", "").strip()
SEM = threading.BoundedSemaphore(16)
STOP = threading.Event()
NATIVE = contextvars.ContextVar("native_bytes", default=0)
original_stream = llm.read_stream


def read_stream(response):
    def inspect():
        for line in response:
            if line.startswith(b"data:") and line[5:].strip() != b"[DONE]":
                try:
                    for choice in json.loads(line[5:]).get("choices", []):
                        delta = choice.get("delta", {})
                        reasoning = delta.get("reasoning_content") or delta.get("reasoning")
                        if isinstance(reasoning, str):
                            NATIVE.set(NATIVE.get() + len(reasoning.encode()))
                except (ValueError, AttributeError):
                    pass
            yield line
    return original_stream(inspect())


llm.read_stream = read_stream


class ArtifactError(RuntimeError):
    pass


class AccessError(RuntimeError):
    pass


def ledger(path):
    filename = path / "calls.jsonl"
    return [json.loads(line) for line in filename.read_text().splitlines()] if filename.is_file() else []


def usage(paths):
    receipts = {(r["session"], r["attempt"]): r for folder in set(paths) for r in ledger(folder)}
    return {
        "calls": len({s for s, _ in receipts}), "attempts": len(receipts),
        "tokens": sum(r.get("usage", {}).get("total_tokens", 0) for r in receipts.values()),
        "go_usd": sum(r.get("allowance") or 0 for r in receipts.values()),
        "charged_usd": sum(r.get("charged_usd") or 0 for r in receipts.values()),
    }


def request(path, prompt):
    if not llm.api_key() or STOP.is_set():
        raise AccessError("DeepSeek is unavailable or OPENCODE_GO_API_KEY is absent")
    if any(item in prompt for item in ("golden_rtl.v", "official_mutants/", "/eval/")):
        raise ValueError("Evaluation source reference in prompt")
    plan = setup()
    tokens = [(llm.LOG_PATH, llm.LOG_PATH.set(path / "calls.jsonl")),
              (llm.THINKING, llm.THINKING.set(PLAN["thought"])),
              (llm.TRANSPORT, llm.TRANSPORT.set({**plan["transport"], "stream": plan["stream"]})),
              (NATIVE, NATIVE.set(0))]
    native = 0
    try:
        with SEM:
            if STOP.is_set():
                raise AccessError("The provider rejected the frozen model")
            reply = llm.call_llm(plan["model"], prompt, plan["temperature"], plan["max_tokens"])
            native = NATIVE.get()
    except llm.LLMError as error:
        history = ledger(path)
        status = history[-1].get("http_status") if history else None
        if status in (400, 401, 402, 403, 404, 422):
            STOP.set()
            raise AccessError(str(error)) from None
        raise ArtifactError(str(error)) from None
    finally:
        for context, value in reversed(tokens):
            context.reset(value)
    if reply["model_actual"] != PLAN["model"]:
        STOP.set()
        raise AccessError("The API returned a different model ID")
    raw = reply.get("response") or ""
    if llm.api_key() in raw:
        STOP.set()
        raise AccessError("Credential match in provider output")
    if not raw.strip():
        raise ArtifactError(f"No final text (finish_reason={reply['finish_reason']})")
    return raw, {"actual_model": reply["model_actual"], "thinking_bytes": native,
                 "finish_reason": reply["finish_reason"]}


def code(raw):
    parts = re.findall(r"```(?:python|py)?\s*\n(.*?)```", raw, re.S | re.I)
    candidates = [*parts, raw]
    for candidate in candidates:
        match = re.search(r"(?m)^def reference\(", candidate)
        if match is None:
            continue
        for body in (candidate.strip() + "\n", candidate[match.start():].strip() + "\n"):
            try:
                ast.parse(body)
            except SyntaxError:
                continue
            return body
    raise ValueError("Return one executable Python reference(vectors) definition")


def relaxed_json(raw):
    decoder = json.JSONDecoder()
    fenced = re.findall(r"```(?:json)?\s*\n(.*?)```", raw, re.S | re.I)
    for candidate in [*fenced, raw]:
        for offset, char in enumerate(candidate):
            if char not in "[{":
                continue
            content = candidate[offset:]
            try:
                return decoder.raw_decode(content)[0]
            except ValueError:
                pass
            try:
                words = list(tokenize.generate_tokens(StringIO(content).readline))
                cleaned = tokenize.untokenize(tok for i, tok in enumerate(words)
                    if not (tok.string == "," and i + 1 < len(words) and words[i + 1].string in ("}", "]")))
                return decoder.raw_decode(cleaned)[0]
            except (ValueError, tokenize.TokenError, IndentationError):
                pass
    raise ValueError("Return the requested complete JSON object or list")


def checkpoint(folder, prompt, decoder, validator=lambda x: x, *, concise=True):
    stamp = folder / "status.json"
    if stamp.is_file():
        state = load(stamp)
        if state["ok"]:
            return load(folder / "value.json")
        raise ArtifactError(f"{folder.name}: {state['errors'][-1]}")
    errors = []
    metas = []
    folder.mkdir(parents=True, exist_ok=True)
    for idx in range(PLAN["format_repairs"] + 1):
        rawfile = folder / f"answer{idx + 1}.txt"
        sent = prompt
        if concise and idx == 0:
            sent += "\nUse brief private deliberation. Prioritize the complete artifact before the token limit."
        if errors:
            sent += "\nFix only the validation problem and return the complete requested artifact. Validation: " + errors[-1]
            if concise:
                sent += "\nUse minimal deliberation and compact final output."
        try:
            if not rawfile.exists():
                raw, meta = request(folder, sent)
                atomic(rawfile, raw)
                save(rawfile.with_suffix(".meta.json"), meta)
            metas.append(load(rawfile.with_suffix(".meta.json")))
            value = validator(decoder(rawfile.read_text()))
        except (ArtifactError, RuntimeError, ValueError, TypeError, KeyError, IndexError,
                AttributeError, subprocess.TimeoutExpired) as error:
            if isinstance(error, AccessError):
                raise
            errors.append(str(error)[:400])
            continue
        save(folder / "value.json", value)
        save(stamp, {"ok": True, "errors": errors, "requests": metas, "selected": rawfile.name})
        return value
    save(stamp, {"ok": False, "errors": errors, "requests": metas})
    raise ArtifactError(f"{folder.name}: {errors[-1]}")
