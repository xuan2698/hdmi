def reference(vectors):
    st = 31
    ans = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            r = row.get('reset', 0)
            clk = row.get('clk', None)
            edge = row.get('edge', None)
            if edge is None and isinstance(clk, str) and ('pos' in clk.lower() or 'neg' in clk.lower()):
                edge = clk
                clk = None
        elif isinstance(row, (list, tuple)):
            r = row[0] if len(row) > 0 else 0
            clk = row[1] if len(row) > 1 else None
            edge = None
            if isinstance(clk, str) and ('pos' in clk.lower() or 'neg' in clk.lower()):
                edge = clk
                clk = None
        else:
            r = row
            clk = None
            edge = None

        if isinstance(r, str):
            s = r.strip().lower()
            if s in ('1', 'true'):
                r = 1
            elif s in ('0', 'false'):
                r = 0
            else:
                r = int(s, 0)
        r = int(r) & 1

        if r:
            st = 31

        if edge is not None:
            if isinstance(edge, str):
                pos = 'pos' in edge.lower()
            else:
                pos = bool(int(edge) & 1)
        elif clk is not None:
            if isinstance(clk, str):
                s = clk.strip().lower()
                if 'pos' in s:
                    pos = True
                elif 'neg' in s:
                    pos = False
                else:
                    cv = int(s, 2) if s in ('0', '1') else int(s, 0)
                    pos = (cv & 1) == 1
            else:
                pos = (int(clk) & 1) == 1
        else:
            pos = (i % 2 == 0)

        cnt = st & 31
        ans.append({
            'cnt_q': cnt,
            'gate_clk_o': 1 if (0 < cnt < 14) else 0,
            'release_reset_o': 1 if (cnt < 8) else 0
        })

        if pos:
            if r:
                st = 31
            elif st > 0:
                st -= 1
    return ans
