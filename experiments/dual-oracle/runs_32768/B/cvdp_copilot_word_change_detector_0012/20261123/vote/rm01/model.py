def reference(vectors):
    state_prev = 0
    state_latched = 0
    state_word = 0
    state_match = 0
    full = (1 << 8) - 1
    result = []

    for idx, row in enumerate(vectors):
        reset = int(row.get('reset', 0)) & 1

        posedge = (idx % 2 == 0)
        if 'edge' in row:
            marker = row['edge']
        elif 'clk' in row:
            marker = row['clk']
        else:
            marker = None

        if marker is not None:
            if isinstance(marker, str):
                s = marker.lower()
                if 'pos' in s or 'rise' in s or s == '1' or s == 'p':
                    posedge = True
                elif 'neg' in s or 'fall' in s or s == '0' or s == 'n':
                    posedge = False
                else:
                    posedge = int(marker) != 0
            else:
                posedge = int(marker) != 0

        if reset:
            state_prev = 0
            state_latched = 0
            state_word = 0
            state_match = 0
            result.append({
                'word_change_pulse': 0,
                'pattern_match_pulse': 0,
                'latched_pattern': 0
            })
            continue

        result.append({
            'word_change_pulse': state_word & 1,
            'pattern_match_pulse': state_match & 1,
            'latched_pattern': state_latched & full
        })

        if posedge:
            data_in = int(row.get('data_in', 0)) & full
            mask = int(row.get('mask', 0)) & full
            match_pattern = int(row.get('match_pattern', 0)) & full
            enable = int(row.get('enable', 0)) & 1
            latch_pattern = int(row.get('latch_pattern', 0)) & 1

            next_prev = data_in
            next_latched = state_latched & full
            if latch_pattern:
                next_latched = match_pattern

            if enable:
                next_word = 1 if (((data_in ^ (state_prev & full)) & mask) != 0) else 0
                next_match = 1 if ((((data_in ^ (state_latched & full)) & mask) == 0)) else 0
            else:
                next_word = 0
                next_match = 0

            state_prev = next_prev & full
            state_latched = next_latched & full
            state_word = next_word & 1
            state_match = next_match & 1

    return result
