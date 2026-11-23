def reference(vectors):
    W = 8
    FULL = (1 << W) - 1
    prev = 0
    latched = 0
    wcp = 0
    pmp = 0
    ans = []

    for row in vectors:
        reset = int(row.get('reset', 0)) & 1
        data_in = int(row.get('data_in', 0)) & FULL
        mask = int(row.get('mask', 0)) & FULL
        match_pattern = int(row.get('match_pattern', 0)) & FULL
        enable = int(row.get('enable', 0)) & 1
        latch_pattern = int(row.get('latch_pattern', 0)) & 1

        if reset:
            prev = 0
            latched = 0
            wcp = 0
            pmp = 0

        ans.append({
            'word_change_pulse': wcp,
            'pattern_match_pulse': pmp,
            'latched_pattern': latched & FULL
        })

        edge = None
        if 'edge' in row:
            edge = row['edge']
        elif 'clk' in row:
            edge = row['clk']
        elif 'clk_edge' in row:
            edge = row['clk_edge']

        is_pos = False
        if edge is not None:
            if isinstance(edge, str):
                s = edge.lower()
                is_pos = ('pos' in s) or ('rise' in s) or s == '1' or s == 'p'
            else:
                is_pos = (int(edge) & 1) == 1

        if is_pos and not reset:
            next_prev = data_in
            next_latched = latched
            if latch_pattern:
                next_latched = match_pattern

            next_wcp = 0
            next_pmp = 0
            if enable:
                if ((data_in ^ prev) & mask) != 0:
                    next_wcp = 1
                if ((data_in ^ latched) & mask) == 0:
                    next_pmp = 1

            prev = next_prev
            latched = next_latched & FULL
            wcp = next_wcp
            pmp = next_pmp

    return ans
