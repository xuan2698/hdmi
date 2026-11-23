def reference(vectors):
    cnt = 31
    result = []
    for i, row in enumerate(vectors):
        expected_pos = (i % 2 == 0)
        expected_clk = 1 if expected_pos else 0
        reset = 0
        edge = None

        if isinstance(row, dict):
            if 'reset' in row:
                reset = row['reset']
            elif 'rst' in row:
                reset = row['rst']
            if 'edge' in row:
                edge = row['edge']
            elif 'clk' in row:
                edge = row['clk']
            else:
                edge = expected_clk

        elif isinstance(row, (list, tuple)):
            n = len(row)
            if n == 0:
                edge = expected_clk
            elif n == 1:
                reset = row[0]
                edge = expected_clk
            else:
                a = row[0]
                b = row[1]
                if isinstance(a, str) and (('pos' in a.lower()) or ('neg' in a.lower())):
                    edge = a
                    reset = b
                elif isinstance(b, str) and (('pos' in b.lower()) or ('neg' in b.lower())):
                    edge = b
                    reset = a
                else:
                    try:
                        ai = int(a) & 1
                        bi = int(b) & 1
                    except:
                        ai = None
                        bi = None
                    if ai == expected_clk and bi != expected_clk:
                        edge = a
                        reset = b
                    elif bi == expected_clk and ai != expected_clk:
                        edge = b
                        reset = a
                    else:
                        edge = a
                        reset = b
        else:
            reset = row
            edge = expected_clk

        if isinstance(reset, str):
            s = reset.strip().lower()
            reset = 1 if s in ('1', 'true', 'high', 'h') else 0
        else:
            reset = 1 if reset else 0

        if isinstance(edge, str):
            s = edge.strip().lower()
            if s in ('posedge', 'pos', 'p', 'rise', 'rising', '1', 'true'):
                pos = True
            elif s in ('negedge', 'neg', 'n', 'fall', 'falling', '0', 'false'):
                pos = False
            else:
                pos = expected_pos
        else:
            if edge is None:
                pos = expected_pos
            else:
                pos = (int(edge) & 1) == 1

        if reset:
            cnt = 31

        cnt_q = cnt & 31
        gate_clk_o = 1 if (cnt_q > 0 and cnt_q < 14) else 0
        release_reset_o = 1 if (cnt_q < 8) else 0

        result.append({
            'cnt_q': cnt_q,
            'gate_clk_o': gate_clk_o,
            'release_reset_o': release_reset_o
        })

        if pos and not reset:
            if cnt > 0:
                cnt = cnt - 1

    return result
