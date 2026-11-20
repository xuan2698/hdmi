import re


def rising_edges(path, clock, signals):
    """Read settled scalar/vector values at each 0-to-1 clock transition."""
    requested = (clock, *signals)
    names, widths, scopes = {}, {}, []
    timescale = ""
    with path.open() as stream:
        for line in stream:
            fields = line.split()
            if not fields:
                continue
            directive = fields[0]
            if directive == "$scope":
                scopes.append(fields[2])
            elif directive == "$upscope":
                scopes.pop()
            elif directive == "$var":
                name = ".".join((*scopes, fields[4]))
                if name in requested:
                    names[name] = fields[3]
                    widths[fields[3]] = int(fields[2])
            elif directive == "$timescale":
                while "$end" not in fields:
                    fields.extend(next(stream).split())
                timescale = "".join(fields[1:-1])
            elif directive == "$enddefinitions":
                break
        missing = set(requested).difference(names)
        if missing:
            raise ValueError(f"{path}: missing VCD signals {sorted(missing)}")
        if not re.fullmatch(r"(1|10|100)(s|ms|us|ns|ps|fs)", timescale):
            raise ValueError(f"{path}: unsupported VCD time unit {timescale}")

        clock_id = names[clock]
        current, samples = {}, []
        tick, last_clock = 0, None

        def sample():
            nonlocal last_clock
            now = current.get(clock_id)
            if last_clock == "0" and now == "1":
                samples.append((tick, {name: current[names[name]] for name in signals}))
            last_clock = now

        for line in stream:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                next_tick = int(line[1:])
                if next_tick < tick:
                    raise ValueError(f"{path}: timestamps out of order")
                if next_tick > tick:
                    sample()
                    tick = next_tick
            elif line[0] in "01xXzZ":
                value, identifier = line[0].lower(), line[1:]
                if identifier in widths:
                    current[identifier] = value
            elif line[0] in "bB":
                value, identifier = line[1:].split()
                if identifier in widths:
                    value = value.lower()
                    fill = value[0] if value[0] in "xz" else "0"
                    current[identifier] = value.rjust(widths[identifier], fill)
        sample()
    if not samples:
        raise ValueError(f"{path}: no rising clock edges")
    return timescale, samples
