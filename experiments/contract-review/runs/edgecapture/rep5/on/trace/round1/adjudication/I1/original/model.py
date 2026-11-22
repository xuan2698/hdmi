def reference(vectors):
    mask = (1 << 32) - 1
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    results = []
    for v in vectors:
        if 'reset' in v:
            cur_reset = v['reset']
        if 'in' in v:
            cur_in = v['in']
        in_val = cur_in & mask
        reset_val = cur_reset & 1
        if reset_val:
            # Rule synchronous_active_high_reset: reset clears out, updates prev_in.
            out = 0
            prev_in = in_val
        else:
            # Rule falling_edge_capture_and_hold: sticky capture of 1->0.
            out = (out | (prev_in & (~in_val & mask))) & mask
            prev_in = in_val
        results.append({'out': out})
        if 'mid' in v:
            mid = v['mid']
            try:
                for k, val in mid.items():
                    if k == 'reset':
                        cur_reset = val
                    elif k == 'in':
                        cur_in = val
            except:
                try:
                    for change in mid:
                        try:
                            for k, val in change.items():
                                if k == 'reset':
                                    cur_reset = val
                                elif k == 'in':
                                    cur_in = val
                        except:
                            pass
                except:
                    pass
    return results
