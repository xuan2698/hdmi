def reference(vectors):
    def gv(row, names, default, pos):
        if isinstance(row, dict):
            for n in names:
                if n in row:
                    v = row[n]
                    if isinstance(v, str):
                        s = v.lower()
                        if s in ('1', 'true', 'high'):
                            return 1
                        if s in ('0', 'false', 'low'):
                            return 0
                    return int(v) & 1
            return default
        if isinstance(row, (list, tuple)):
            if len(row) > pos and not isinstance(row[0], str):
                v = row[pos]
            elif len(row) > pos + 1:
                v = row[pos + 1]
            elif len(row) > pos:
                v = row[pos]
            else:
                return default
            if isinstance(v, str):
                s = v.lower()
                if 'pos' in s or 'neg' in s:
                    return default
                if s in ('1', 'true', 'high'):
                    return 1
                if s in ('0', 'false', 'low'):
                    return 0
            return int(v) & 1
        return default

    def ge(row, idx):
        if isinstance(row, dict):
            for k in ('edge', 'clk', 'clock'):
                if k in row:
                    v = row[k]
                    if isinstance(v, str):
                        s = v.lower()
                        if 'pos' in s:
                            return 1
                        if 'neg' in s:
                            return 0
                    return 1 if v else 0
        elif isinstance(row, (list, tuple)):
            for v in row:
                if isinstance(v, str):
                    s = v.lower()
                    if 'pos' in s:
                        return 1
                    if 'neg' in s:
                        return 0
            if len(row) >= 3 and not isinstance(row[0], str):
                v = row[0]
                if v in (0, 1, False, True):
                    return 1 if v else 0
        return 1 if idx % 2 == 0 else 0

    div = 0
    pulse = 0
    sec = 0
    mins = 0
    hr = 0
    out = []

    for idx, row in enumerate(vectors):
        rst = gv(row, ('reset', 'rst'), 0, 0)
        start = gv(row, ('start_stop', 'startstop', 'start'), 0, 1)
        edge = ge(row, idx)

        if rst:
            div = 0
            pulse = 0
            sec = 0
            mins = 0
            hr = 0

        out.append({'seconds': sec & 63, 'minutes': mins & 63, 'hour': hr & 1})

        if edge:
            if rst:
                div = 0
                pulse = 0
                sec = 0
                mins = 0
                hr = 0
            else:
                np = 1 if div == 3 else 0
                nd = 0 if div == 3 else div + 1
                ns = sec
                nm = mins
                nh = hr

                if pulse and start:
                    if sec == 59:
                        ns = 0
                        if mins == 59:
                            nm = 0
                            nh = 1
                        else:
                            nm = mins + 1
                    else:
                        ns = sec + 1

                div = nd
                pulse = np
                sec = ns
                mins = nm
                hr = nh

    return out
