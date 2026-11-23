def reference(vectors):
    tr, tok, dout = 1, 0, 0
    res = []
    for i, row in enumerate(vectors):
        if isinstance(row, dict):
            edge = row.get('edge', row.get('clk', row.get('edge_type', None)))
            rst = int(row.get('rst', 0))
            din = int(row.get('data_in', 0)) & 0xF
            hd = int(row.get('has_data_to_send', 0)) & 1
        else:
            edge = row[0] if len(row) > 0 else None
            rst = int(row[1]) if len(row) > 1 else 0
            din = int(row[2]) & 0xF if len(row) > 2 else 0
            hd = int(row[3]) & 1 if len(row) > 3 else 0

        if edge is None:
            pos = (i % 2 == 0)
        elif isinstance(edge, str):
            e = edge.lower()
            if 'pos' in e or e in ('1', 'p', 'rise', 'rising'):
                pos = True
            elif 'neg' in e or e in ('0', 'n', 'fall', 'falling'):
                pos = False
            else:
                pos = (i % 2 == 0)
        else:
            pos = bool(edge)

        if rst == 1:
            tr, tok, dout = 1, 0, 0

        res.append({'data_out': dout, 'token_received': tr, 'token': tok})

        if pos and rst == 0:
            ot = tr
            if ot == 1:
                nt = 2
            elif ot == 2:
                nt = 4
            elif ot == 4:
                nt = 8
            elif ot == 8:
                nt = 1
            else:
                nt = 1

            if ot in (1, 2, 4, 8):
                ntok = ot
                valid = True
            else:
                ntok = 0
                valid = False

            ndout = (din if (hd and valid) else 0) & 0xF
            tr, tok, dout = nt, ntok, ndout

    return res
