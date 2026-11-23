def reference(vectors):
    W = 8
    M = (1 << W) - 1
    prev = 0
    latched = 0
    wcp = 0
    pmp = 0
    outs = []
    for i, row in enumerate(vectors):
        reset = row.get('reset', 0)
        data = row.get('data_in', 0) & M
        mask = row.get('mask', M) & M
        match_pattern = row.get('match_pattern', 0) & M
        enable = row.get('enable', 0)
        latch_pattern = row.get('latch_pattern', 0)

        e = row.get('edge', None)
        if e is None and 'clk' in row:
            e = row['clk']
        if e is None:
            is_pos = (i % 2 == 0)
        elif isinstance(e, str):
            el = e.lower()
            is_pos = el.startswith('pos') or el == 'p' or el == '1'
        else:
            is_pos = bool(e)

        if reset:
            prev = 0
            latched = 0
            wcp = 0
            pmp = 0

        outs.append({
            'word_change_pulse': wcp & 1,
            'pattern_match_pulse': pmp & 1,
            'latched_pattern': latched & M
        })

        if not reset and is_pos:
            change = ((data ^ prev) & mask & M) != 0
            match_cond = ((data & mask & M) == (latched & mask & M))
            wcp = 1 if (enable and change) else 0
            pmp = 1 if (enable and match_cond) else 0
            latched = (match_pattern if latch_pattern else latched) & M
            prev = data & M

    return outs
