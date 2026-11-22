def reference(vectors):
    mask = (1 << 32) - 1
    out_state = 0
    prev_in = 0
    current = {'reset': 0, 'in': 0}
    results = []

    for row in vectors:
        # Apply explicitly driven row inputs before the sampled posedge; these override carried mid changes.
        if 'reset' in row:
            current['reset'] = row['reset'] & 1
        if 'in' in row:
            current['in'] = row['in'] & mask

        rst = current['reset']
        inp = current['in'] & mask

        # reset_clear: synchronous active-high reset has priority and clears out on this posedge.
        # capture_fall candidate interpretation: also clear/ignore prev_in while reset is high.
        if rst == 1:
            out_state = 0
            prev_in = 0
        else:
            # capture_fall: out[j] becomes 1 when prev_in[j] == 1 and in[j] == 0.
            fall = prev_in & (~inp & mask)
            # hold_state: all non-falling bits hold previous out value.
            out_state = (out_state | fall) & mask
            # prev_in tracks the sampled input on normal posedges.
            prev_in = inp

        results.append({'out': out_state})

        # mid changes occur after the row's posedge sampling and are carried to the next row.
        mid = row.get('mid')
        if mid:
            for key, value in mid.items():
                if key == 'reset':
                    current['reset'] = value & 1
                elif key == 'in':
                    current['in'] = value & mask
                else:
                    current[key] = value

    return results
