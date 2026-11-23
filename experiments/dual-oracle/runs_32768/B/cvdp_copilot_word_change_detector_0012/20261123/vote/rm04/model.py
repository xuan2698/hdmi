def reference(vectors):
    W = 8
    M = (1 << W) - 1
    data_prev = 0
    latched = 0
    word_change_pulse = 0
    pattern_match_pulse = 0
    out = []

    for row in vectors:
        reset = int(row.get('reset', 0)) & 1
        data_in = int(row.get('data_in', 0)) & M
        mask = int(row.get('mask', 0)) & M
        match_pattern = int(row.get('match_pattern', 0)) & M
        enable = int(row.get('enable', 0)) & 1
        latch_pattern = int(row.get('latch_pattern', 0)) & 1

        edge = row.get('edge', 1)
        if isinstance(edge, str):
            is_posedge = 'pos' in edge.lower()
        else:
            is_posedge = bool(edge)

        if reset:
            data_prev = 0
            latched = 0
            word_change_pulse = 0
            pattern_match_pulse = 0
            out.append({
                'word_change_pulse': 0,
                'pattern_match_pulse': 0,
                'latched_pattern': 0
            })
            continue

        out.append({
            'word_change_pulse': word_change_pulse,
            'pattern_match_pulse': pattern_match_pulse,
            'latched_pattern': latched
        })

        if is_posedge:
            next_word_change_pulse = 1 if enable and (((data_in ^ data_prev) & mask) != 0) else 0
            next_pattern_match_pulse = 1 if enable and (((data_in ^ latched) & mask) == 0) else 0
            if latch_pattern:
                latched = match_pattern & M
            word_change_pulse = next_word_change_pulse
            pattern_match_pulse = next_pattern_match_pulse
            data_prev = data_in

    return out
