def reference(vectors):
    data_prev = 0
    latched = 0
    wcp = 0
    pmp = 0
    cur_reset = 0
    cur_data = 0
    cur_mask = 0
    cur_match = 0
    cur_enable = 0
    cur_latch = 0
    result = []
    for i, row in enumerate(vectors):
        if 'reset' in row:
            cur_reset = row['reset'] & 1
        if 'data_in' in row:
            cur_data = row['data_in'] & 255
        if 'mask' in row:
            cur_mask = row['mask'] & 255
        if 'match_pattern' in row:
            cur_match = row['match_pattern'] & 255
        if 'enable' in row:
            cur_enable = row['enable'] & 1
        if 'latch_pattern' in row:
            cur_latch = row['latch_pattern'] & 1

        edge = 'pos' if (i % 2 == 0) else 'neg'
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                if 'pos' in e or 'rise' in e or e.startswith('p'):
                    edge = 'pos'
                elif 'neg' in e or 'fall' in e or e.startswith('n'):
                    edge = 'neg'
            else:
                edge = 'pos' if e else 'neg'

        if cur_reset:
            data_prev = 0
            latched = 0
            wcp = 0
            pmp = 0

        result.append({
            'word_change_pulse': wcp & 1,
            'pattern_match_pulse': pmp & 1,
            'latched_pattern': latched & 255
        })

        if edge == 'pos' and not cur_reset:
            changed = ((cur_data ^ data_prev) & cur_mask) != 0
            next_wcp = 1 if (cur_enable and changed) else 0
            match = ((cur_data ^ latched) & cur_mask) == 0
            next_pmp = 1 if (cur_enable and match) else 0
            next_latched = cur_match if cur_latch else latched

            data_prev = cur_data
            wcp = next_wcp
            pmp = next_pmp
            latched = next_latched

    return result
