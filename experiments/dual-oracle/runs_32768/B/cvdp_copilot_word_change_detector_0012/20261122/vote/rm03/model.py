def reference(vectors):
    latched = 0
    prev = 0
    word_pulse = 0
    match_pulse = 0
    out = []

    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            reset = int(row.get('reset', 0)) & 1
            data_in = int(row.get('data_in', 0)) & 0xFF
            mask = int(row.get('mask', 0)) & 0xFF
            match_pattern = int(row.get('match_pattern', 0)) & 0xFF
            enable = int(row.get('enable', 0)) & 1
            latch_pattern = int(row.get('latch_pattern', 0)) & 1

            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    is_pos = e.lower().startswith('pos') or e == '1'
                else:
                    is_pos = (e == 1 or e is True)
            elif 'clk' in row:
                is_pos = int(row['clk']) == 1
            else:
                is_pos = (i % 2 == 0)
        else:
            r = list(row)
            if len(r) == 7:
                e = r[0]
                if isinstance(e, str):
                    is_pos = e.lower().startswith('pos') or e == '1'
                else:
                    is_pos = (e == 1 or e is True)
                reset = int(r[1]) & 1
                data_in = int(r[2]) & 0xFF
                mask = int(r[3]) & 0xFF
                match_pattern = int(r[4]) & 0xFF
                enable = int(r[5]) & 1
                latch_pattern = int(r[6]) & 1
            else:
                is_pos = (i % 2 == 0)
                reset = int(r[0]) & 1
                data_in = int(r[1]) & 0xFF
                mask = int(r[2]) & 0xFF
                match_pattern = int(r[3]) & 0xFF
                enable = int(r[4]) & 1
                latch_pattern = int(r[5]) & 1

        if reset:
            latched = 0
            prev = 0
            word_pulse = 0
            match_pulse = 0

        out.append({
            'word_change_pulse': int(word_pulse) & 1,
            'pattern_match_pulse': int(match_pulse) & 1,
            'latched_pattern': int(latched) & 0xFF
        })

        if is_pos and not reset:
            next_word = 1 if (enable and (((data_in ^ prev) & mask) != 0)) else 0
            next_match = 1 if (enable and (((data_in ^ latched) & mask) == 0)) else 0

            if latch_pattern:
                latched = match_pattern & 0xFF

            prev = data_in & 0xFF
            word_pulse = next_word
            match_pulse = next_match

    return out
