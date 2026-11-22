def reference(vectors):
    # Contract state: registered output Q, initially Q0 (0) since no reset.
    Q = 0
    # Carried input state after mid changes.
    cur_L = 0
    cur_q_in = 0
    cur_r_in = 0
    result = []

    for row in vectors:
        # Start from carried inputs, then apply this row's values before the edge.
        L = cur_L
        q_in = cur_q_in
        r_in = cur_r_in

        try:
            if 'L' in row:
                L = row['L'] & 1
            if 'q_in' in row:
                q_in = row['q_in'] & 1
            if 'r_in' in row:
                r_in = row['r_in'] & 1
            if 'inputs' in row:
                inp = row['inputs']
                if 'L' in inp:
                    L = inp['L'] & 1
                if 'q_in' in inp:
                    q_in = inp['q_in'] & 1
                if 'r_in' in inp:
                    r_in = inp['r_in'] & 1
        except:
            pass

        # Rule Q_posedge_update, with candidate interpretation:
        # at posedge, if L=1 Q <= r_in; otherwise hold previous Q.
        if L == 1:
            Q = r_in & 1
        else:
            Q = Q & 1

        result.append({'Q': Q})

        # Inputs just sampled become the held values until mid changes.
        cur_L = L
        cur_q_in = q_in
        cur_r_in = r_in

        # Mid changes occur AFTER sampling and carry into the next row.
        try:
            if 'mid' in row:
                mid = row['mid']

                # mid as a mapping of signal name to value.
                for k in ('L', 'q_in', 'r_in'):
                    try:
                        v = mid[k] & 1
                        if k == 'L':
                            cur_L = v
                        elif k == 'q_in':
                            cur_q_in = v
                        else:
                            cur_r_in = v
                    except:
                        pass

                # mid as a list of mappings or (name, value) pairs.
                try:
                    for item in mid:
                        for k in ('L', 'q_in', 'r_in'):
                            try:
                                v = item[k] & 1
                                if k == 'L':
                                    cur_L = v
                                elif k == 'q_in':
                                    cur_q_in = v
                                else:
                                    cur_r_in = v
                            except:
                                pass

                        try:
                            k = item[0]
                            v = item[1] & 1
                            if k == 'L':
                                cur_L = v
                            elif k == 'q_in':
                                cur_q_in = v
                            elif k == 'r_in':
                                cur_r_in = v
                        except:
                            pass
                except:
                    pass
        except:
            pass

    return result
