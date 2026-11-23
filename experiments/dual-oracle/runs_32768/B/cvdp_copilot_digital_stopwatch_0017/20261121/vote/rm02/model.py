def reference(vectors):
    sec = 0
    mins = 0
    hr = 0
    cnt = 0
    out = []
    if isinstance(vectors, dict):
        keys = list(vectors.keys())
        n = len(vectors[keys[0]]) if keys else 0
        rows = []
        for i in range(n):
            d = {}
            for k in keys:
                d[k] = vectors[k][i]
            rows.append(d)
        vectors = rows
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            reset = row.get('reset', 0)
            start = row.get('start_stop', 0)
            if 'edge' in row:
                e = row['edge']
            elif 'clk' in row:
                e = row['clk']
            else:
                e = 1 - (i & 1)
        else:
            if len(row) >= 3:
                e = row[0]
                reset = row[1]
                start = row[2]
            elif len(row) == 2:
                e = 1 - (i & 1)
                reset = row[0]
                start = row[1]
            else:
                e = 1 - (i & 1)
                reset = row[0] if len(row) > 0 else 0
                start = 0
        if isinstance(e, str):
            pos = (e and e[0].lower() == 'p') or e == '1'
        else:
            pos = int(e) != 0
        reset = int(reset) & 1
        start = int(start) & 1
        if reset:
            sec = 0
            mins = 0
            hr = 0
            cnt = 0
        out.append({'seconds': sec, 'minutes': mins, 'hour': hr})
        if pos and not reset and start:
            if cnt >= 3:
                cnt = 0
                if sec == 59:
                    sec = 0
                    if mins == 59:
                        mins = 0
                        hr = 1
                    else:
                        mins += 1
                else:
                    sec += 1
            else:
                cnt += 1
    return out
