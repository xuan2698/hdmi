def reference(vectors):
    # Sequential modulo-8 counter gated by an armed flag.
    # q initial = 4, flag initial = 0.
    # On each posedge (sample after edge settles):
    #   if a == 1: q holds, flag = 1
    #   else (a == 0): if flag == 1: q = (q + 1) % 8; flag stays 1
    #                  else: q holds, flag stays 0
    # Mid changes occur after sampling and carry to next row.
    q = 4
    flag = 0
    out = []
    for row in vectors:
        clk = row.get('clk')
        a = row.get('a')
        # Sample on posedge (clk == 1)
        if clk == 1:
            if a == 1:
                flag = 1
                # q holds
            else:
                if flag == 1:
                    q = (q + 1) % 8
                # flag stays
        out.append({'q': q & 0x7})
    return out
