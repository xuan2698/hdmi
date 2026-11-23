def reference(vectors):
    cnt = 31
    out = []

    def dget(row, name, default=None):
        if name in row:
            return row[name]
        for k, v in row.items():
            if str(k).lower() == name:
                return v
        return default

    for i, row in enumerate(vectors):
        reset = 0
        edge = None

        if isinstance(row, dict):
            rv = dget(row, 'reset', None)
            if rv is None:
                rv = dget(row, 'rst', 0)
            reset = int(rv)

            ev = dget(row, 'edge', None)
            if ev is not None:
                s = str(ev).lower()
                if 'pos' in s or s == '1':
                    edge = 'pos'
                elif 'neg' in s or s == '0':
                    edge = 'neg'

            if edge is None:
                cv = dget(row, 'clk', None)
                if cv is None:
                    cv = dget(row, 'clock', None)
                if cv is not None:
                    s = str(cv).lower()
                    if 'pos' in s or s == '1':
                        edge = 'pos'
                    elif 'neg' in s or s == '0':
                        edge = 'neg'
                    else:
                        try:
                            edge = 'pos' if int(cv) != 0 else 'neg'
                        except Exception:
                            edge = None

            if edge is None:
                edge = 'pos' if i % 2 == 0 else 'neg'
        else:
            n = len(row)
            if n == 0:
                reset = 0
                edge = 'pos' if i % 2 == 0 else 'neg'
            elif n == 1:
                reset = int(row[0])
                edge = 'pos' if i % 2 == 0 else 'neg'
            else:
                v0 = row[0]
                v1 = row[1]

                if isinstance(v0, str) and ('pos' in v0.lower() or 'neg' in v0.lower() or 'edge' in v0.lower()):
                    s = v0.lower()
                    if 'pos' in s or s == '1':
                        edge = 'pos'
                    elif 'neg' in s or s == '0':
                        edge = 'neg'
                    reset = int(v1)
                elif isinstance(v1, str) and ('pos' in v1.lower() or 'neg' in v1.lower()):
                    s = v1.lower()
                    edge = 'pos' if 'pos' in s else 'neg'
                    reset = int(v0)
                else:
                    try:
                        v0i = int(v0)
                    except Exception:
                        v0i = None
                    try:
                        v1i = int(v1)
                    except Exception:
                        v1i = None

                    exp = 1 if i % 2 == 0 else 0
                    if v0i is not None and v0i == exp and (v1i is None or v1i != exp):
                        clk = v0i
                        reset = v1i if v1i is not None else 0
                    elif v1i is not None and v1i == exp and (v0i is None or v0i != exp):
                        reset = v0i if v0i is not None else 0
                        clk = v1i
                    else:
                        clk = v0i if v0i is not None else 0
                        reset = v1i if v1i is not None else 0

                    edge = 'pos' if clk == 1 else 'neg'

        reset = int(reset)
        if reset == 1:
            cnt = 31

        gate = 1 if (0 < cnt < 14) else 0
        rel = 1 if cnt < 8 else 0
        out.append({'cnt_q': cnt, 'gate_clk_o': gate, 'release_reset_o': rel})

        if edge == 'pos':
            if reset == 0:
                if cnt > 0:
                    cnt -= 1
            else:
                cnt = 31

    return out
