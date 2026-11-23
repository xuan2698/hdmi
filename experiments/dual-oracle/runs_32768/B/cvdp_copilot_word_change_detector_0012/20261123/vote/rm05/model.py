def reference(vectors):
    latched = 0
    prev = 0
    wcp = 0
    pmp = 0
    out = []
    posedge = True
    for row in vectors:
        reset = int(row.get("reset", 0)) & 1
        data = int(row.get("data_in", 0)) & 255
        mask = int(row.get("mask", 0)) & 255
        match = int(row.get("match_pattern", 0)) & 255
        enable = int(row.get("enable", 0)) & 1
        latch = int(row.get("latch_pattern", 0)) & 1
        edge = row.get("edge", None)
        ispos = posedge
        if edge is not None:
            text = str(edge).lower()
            if edge == 1 or edge == True or "pos" in text or "rise" in text:
                ispos = True
            elif edge == 0 or edge == False or "neg" in text or "fall" in text:
                ispos = False
        if reset == 1:
            latched = 0
            prev = 0
            wcp = 0
            pmp = 0
        out.append({"word_change_pulse": wcp, "pattern_match_pulse": pmp, "latched_pattern": latched})
        if ispos and reset == 0:
            diff = 1 if ((data ^ prev) & mask) != 0 else 0
            cond = 1 if ((data ^ latched) & mask) == 0 else 0
            wcp = 1 if enable and diff else 0
            pmp = 1 if enable and cond else 0
            if latch:
                latched = match
            prev = data
        posedge = not ispos
    return out
