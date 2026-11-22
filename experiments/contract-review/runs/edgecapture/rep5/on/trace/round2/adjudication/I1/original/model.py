def reference(vectors):
    # State: out is 32-bit sticky capture; prev_in is previous sampled in.
    # Power-up unspecified; choose concrete zeros for determinism.
    out = 0
    prev_in = 0
    cur_reset = 0
    cur_in = 0
    results = []
    for row in vectors:
        # Drive row values before the sampled posedge.
        try:
            v = row.get('reset')
            if v is not None:
                cur_reset = v & 1
        except:
            try:
                cur_reset = row[0] & 1
            except:
                pass
        try:
            v = row.get('in')
            if v is not None:
                cur_in = v & 0xFFFFFFFF
        except:
            try:
                cur_in = row[1] & 0xFFFFFFFF
            except:
                pass

        # synchronous_active_high_reset: reset==1 at posedge clears out, priority over capture.
        # falling_edge_capture_and_hold: reset==0 captures 1-to-0 transitions and holds existing 1s.
        # prev_in is updated every posedge, including reset cycles.
        if cur_reset:
            out = 0
            prev_in = cur_in
        else:
            falling = prev_in & ((~cur_in) & 0xFFFFFFFF)
            out = (out | falling) & 0xFFFFFFFF
            prev_in = cur_in

        results.append({'out': out})

        # Optional mid input changes occur AFTER sampling, before the next row.
        mid = None
        try:
            mid = row.get('mid')
        except:
            try:
                mid = row[2]
            except:
                pass
        if mid is not None:
            try:
                v = mid.get('reset')
                if v is not None:
                    cur_reset = v & 1
            except:
                try:
                    v = mid[0]
                    if v is not None:
                        cur_reset = v & 1
                except:
                    pass
            try:
                v = mid.get('in')
                if v is not None:
                    cur_in = v & 0xFFFFFFFF
            except:
                try:
                    v = mid[1]
                    if v is not None:
                        cur_in = v & 0xFFFFFFFF
                except:
                    try:
                        cur_in = mid & 0xFFFFFFFF
                    except:
                        pass
        # Alternate mid key names.
        try:
            v = row.get('mid_reset')
            if v is not None:
                cur_reset = v & 1
        except:
            pass
        try:
            v = row.get('mid_in')
            if v is not None:
                cur_in = v & 0xFFFFFFFF
        except:
            pass
    return results
