def reference(vectors):
    DW = 8
    FM = (1 << DW) - 1
    latched = 0
    data_prev = 0
    word_change_pulse = 0
    pattern_match_pulse = 0
    out = []

    def getv(row, name, default=0):
        if isinstance(row, dict) and name in row:
            return row[name]
        return default

    def toint(x):
        if isinstance(x, str):
            s = x.strip().lower()
            if s.startswith("0b"):
                return int(s[2:], 2)
            if s.startswith("0x"):
                return int(s[2:], 16)
            try:
                return int(s, 0)
            except:
                return int(s)
        return int(x)

    def is_posedge(row):
        e = None
        if isinstance(row, dict):
            for k in ("edge", "clk_edge", "edge_type", "event"):
                if k in row:
                    e = row[k]
                    break
            if e is None and "clk" in row:
                e = row["clk"]
            if row.get("posedge", False):
                return True
            if row.get("negedge", False):
                return False
        if isinstance(e, str):
            s = e.strip().lower()
            return ("pos" in s) or ("rise" in s) or (s == "1")
        if e is not None:
            try:
                return (toint(e) & 1) == 1
            except:
                return False
        return False

    for row in vectors:
        reset = toint(getv(row, "reset", 0)) & 1

        if reset:
            latched = 0
            data_prev = 0
            word_change_pulse = 0
            pattern_match_pulse = 0
            out.append({
                "word_change_pulse": 0,
                "pattern_match_pulse": 0,
                "latched_pattern": 0
            })
            continue

        out.append({
            "word_change_pulse": word_change_pulse,
            "pattern_match_pulse": pattern_match_pulse,
            "latched_pattern": latched & FM
        })

        if is_posedge(row):
            data_in = toint(getv(row, "data_in", 0)) & FM
            mask = toint(getv(row, "mask", 0)) & FM
            match_pattern = toint(getv(row, "match_pattern", 0)) & FM
            enable = toint(getv(row, "enable", 0)) & 1
            latch_pattern = toint(getv(row, "latch_pattern", 0)) & 1

            if enable:
                next_word_change_pulse = 1 if (((data_in ^ data_prev) & mask) != 0) else 0
                next_pattern_match_pulse = 1 if (((data_in ^ latched) & mask) == 0) else 0
            else:
                next_word_change_pulse = 0
                next_pattern_match_pulse = 0

            data_prev = data_in
            if latch_pattern:
                latched = match_pattern

            word_change_pulse = next_word_change_pulse
            pattern_match_pulse = next_pattern_match_pulse

    return out
