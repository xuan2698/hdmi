def reference(vectors):
    latched_pattern = 0
    data_in_prev = 0
    word_change_pulse = 0
    pattern_match_pulse = 0
    out = []
    idx = 0
    for row in vectors:
        reset = int(row.get('reset', 0)) & 1
        data_in = int(row.get('data_in', 0)) & 0xFF
        mask = int(row.get('mask', 0)) & 0xFF
        match_pattern = int(row.get('match_pattern', 0)) & 0xFF
        enable = int(row.get('enable', 0)) & 1
        latch_pattern = int(row.get('latch_pattern', 0)) & 1

        if reset:
            latched_pattern = 0
            data_in_prev = 0
            word_change_pulse = 0
            pattern_match_pulse = 0

        edge = row.get('edge', None)
        if edge is None:
            edge = row.get('clk_edge', None)

        if edge is None:
            is_pos = (idx % 2 == 0)
        else:
            if isinstance(edge, str):
                is_pos = ('pos' in edge.lower())
            else:
                is_pos = (int(edge) != 0)

        out.append({
            'word_change_pulse': word_change_pulse & 1,
            'pattern_match_pulse': pattern_match_pulse & 1,
            'latched_pattern': latched_pattern & 0xFF
        })

        if is_pos and reset == 0:
            old_latched_pattern = latched_pattern

            change = 1 if (((data_in ^ data_in_prev) & mask) != 0) else 0
            match = 1 if (((data_in ^ old_latched_pattern) & mask) == 0) else 0

            if enable:
                word_change_pulse = change
                pattern_match_pulse = match
            else:
                word_change_pulse = 0
                pattern_match_pulse = 0

            if latch_pattern:
                latched_pattern = match_pattern

            data_in_prev = data_in

        idx += 1

    return out
