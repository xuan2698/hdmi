def reference(vectors):
    cnt = 31
    result = []
    prev_clk = None

    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            r = row.get('reset', 0)
            e = row.get('edge', None)
            c = row.get('clk', None)
        else:
            r = 0
            e = None
            c = None
            if isinstance(row, (list, tuple)):
                if len(row) == 1:
                    r = row[0]
                else:
                    if isinstance(row[0], str):
                        e = row[0]
                        r = row[1] if len(row) > 1 else 0
                    else:
                        r = row[-1]
            else:
                r = row

        if isinstance(r, str):
            reset = 1 if r.strip().lower() in ('1', 'true', 'yes', 'high') else 0
        else:
            reset = 1 if r else 0

        if e is None and c is not None:
            if prev_clk is None:
                e = 'posedge' if c else 'negedge'
            elif c and not prev_clk:
                e = 'posedge'
            elif not c and prev_clk:
                e = 'negedge'
            else:
                e = 'none'
            prev_clk = c
        elif e is None:
            e = 'posedge' if i % 2 == 0 else 'negedge'

        edge = str(e).strip().lower()

        if reset:
            cnt = 31

        gate = 1 if (cnt > 0 and cnt < 14) else 0
        release = 1 if cnt < 8 else 0
        result.append({'cnt_q': cnt, 'gate_clk_o': gate, 'release_reset_o': release})

        if edge in ('posedge', 'p', '1', 'true', 'rising', 'rise'):
            if reset:
                cnt = 31
            else:
                if cnt > 0:
                    cnt -= 1

    return result
