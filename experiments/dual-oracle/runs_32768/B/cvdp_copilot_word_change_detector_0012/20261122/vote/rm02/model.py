def reference(vectors):
    DW = 8
    M = (1 << DW) - 1
    prev = 0
    latched = 0
    wcp = 0
    pmp = 0
    out = []
    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            reset = int(row.get('reset', 0)) & 1
            data_in = int(row.get('data_in', 0)) & M
            mask = int(row.get('mask', 0)) & M
            match_pattern = int(row.get('match_pattern', 0)) & M
            enable = int(row.get('enable', 0)) & 1
            latch_pattern = int(row.get('latch_pattern', 0)) & 1
            posedge = None
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    posedge = ('pos' in e.lower()) or (e == '1')
                else:
                    posedge = bool(int(e))
            elif 'clk' in row:
                posedge = (int(row['clk']) & 1) == 1
            elif 'posedge' in row:
                posedge = bool(int(row['posedge']))
            elif 'negedge' in row:
                posedge = not bool(int(row['negedge']))
            if posedge is None:
                posedge = (idx % 2 == 0)
        else:
            if len(row) >= 7:
                clk = int(row[0]) & 1
                reset = int(row[1]) & 1
                data_in = int(row[2]) & M
                mask = int(row[3]) & M
                match_pattern = int(row[4]) & M
                enable = int(row[5]) & 1
                latch_pattern = int(row[6]) & 1
                posedge = (clk == 1)
            else:
                reset = int(row[0]) & 1
                data_in = int(row[1]) & M
                mask = int(row[2]) & M
                match_pattern = int(row[3]) & M
                enable = int(row[4]) & 1
                latch_pattern = int(row[5]) & 1
                posedge = (idx % 2 == 0)

        if reset:
            prev = 0
            latched = 0
            wcp = 0
            pmp = 0

        out.append({
            'word_change_pulse': wcp,
            'pattern_match_pulse': pmp,
            'latched_pattern': latched & M
        })

        if posedge and not reset:
            changed = ((data_in ^ prev) & mask) != 0
            matched = ((data_in & mask) == (latched & mask))
            new_wcp = 1 if (enable and changed) else 0
            new_pmp = 1 if (enable and matched) else 0
            if latch_pattern:
                latched = match_pattern & M
            prev = data_in
            wcp = new_wcp
            pmp = new_pmp

    return out
