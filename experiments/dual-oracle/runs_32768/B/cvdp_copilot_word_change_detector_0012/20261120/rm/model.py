def reference(vectors):
    prev = 0
    latched = 0
    word = 0
    pat = 0
    out = []
    for i, row in enumerate(vectors):
        rst = int(row.get('reset', 0)) & 1
        data = int(row.get('data_in', 0)) & 255
        mask = int(row.get('mask', 0)) & 255
        match = int(row.get('match_pattern', 0)) & 255
        en = int(row.get('enable', 0)) & 1
        lp = int(row.get('latch_pattern', 0)) & 1

        edge = row.get('edge', None)
        if edge is None:
            if 'posedge' in row:
                pos = bool(row['posedge'])
            elif 'clk' in row:
                c = row['clk']
                if isinstance(c, str):
                    e = c.lower()
                    if 'pos' in e:
                        pos = True
                    elif 'neg' in e:
                        pos = False
                    else:
                        try:
                            pos = (int(c) & 1) == 1
                        except:
                            pos = (i % 2 == 0)
                else:
                    pos = (int(c) & 1) == 1
            else:
                pos = (i % 2 == 0)
        else:
            if isinstance(edge, str):
                e = edge.lower()
                if 'pos' in e:
                    pos = True
                elif 'neg' in e:
                    pos = False
                else:
                    try:
                        pos = (int(edge) & 1) == 1
                    except:
                        pos = (i % 2 == 0)
            else:
                pos = bool(edge)

        if rst:
            prev = 0
            latched = 0
            word = 0
            pat = 0

        out.append({
            'word_change_pulse': word & 1,
            'pattern_match_pulse': pat & 1,
            'latched_pattern': latched & 255
        })

        if rst:
            prev = 0
            latched = 0
            word = 0
            pat = 0
        elif pos:
            new_latched = match if lp else latched
            new_word = 1 if (en and (((data ^ prev) & mask) != 0)) else 0
            new_pat = 1 if (en and (((data ^ latched) & mask) == 0)) else 0
            word = new_word
            pat = new_pat
            latched = new_latched & 255
            prev = data & 255

    return out
