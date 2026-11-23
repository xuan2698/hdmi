def reference(vectors):
    st = 0
    opa = 0
    opb = 0
    res = 0
    ovf = 0
    out = []
    row_idx = 0
    prev_clk = None

    def gv(row, name, default=0):
        if isinstance(row, dict) and name in row:
            return row[name]
        return default

    for row in vectors:
        rst = int(gv(row, 'i_rst_n', 1)) & 1
        clr = int(gv(row, 'i_clear', 0)) & 1
        en = int(gv(row, 'i_enable', 0)) & 1
        start = int(gv(row, 'i_start', 0)) & 1
        mode = int(gv(row, 'i_mode', 0)) & 1
        a = int(gv(row, 'i_operand_a', 0)) & 0xFF
        b = int(gv(row, 'i_operand_b', 0)) & 0xFF

        edge = None
        if isinstance(row, dict) and ('edge' in row):
            e = row['edge']
            if isinstance(e, str):
                s = e.lower()
                if 'pos' in s:
                    edge = 'pos'
                elif 'neg' in s:
                    edge = 'neg'
                else:
                    edge = 'pos' if row_idx % 2 == 0 else 'neg'
            else:
                try:
                    edge = 'pos' if int(e) != 0 else 'neg'
                except:
                    edge = 'pos' if row_idx % 2 == 0 else 'neg'
        elif isinstance(row, dict) and ('i_clk' in row):
            clk = int(row['i_clk']) & 1
            if prev_clk is None:
                edge = 'pos' if clk == 1 else 'neg'
            else:
                if prev_clk == 0 and clk == 1:
                    edge = 'pos'
                elif prev_clk == 1 and clk == 0:
                    edge = 'neg'
                else:
                    edge = 'pos' if row_idx % 2 == 0 else 'neg'
            prev_clk = clk
        else:
            edge = 'pos' if row_idx % 2 == 0 else 'neg'

        if rst == 0:
            st = 0
            opa = 0
            opb = 0
            res = 0
            ovf = 0

        out.append({
            'o_resultant_sum': res & 0xFF,
            'o_overflow': ovf & 1,
            'o_ready': 1 if st == 3 else 0,
            'o_status': st & 3
        })

        if edge == 'pos':
            if rst == 0:
                st = 0
                opa = 0
                opb = 0
                res = 0
                ovf = 0
            elif clr == 1:
                st = 0
                res = 0
                ovf = 0
            else:
                if st == 0:
                    if en == 1 and start == 1:
                        st = 1
                elif st == 1:
                    opa = a
                    opb = b
                    st = 2
                elif st == 2:
                    sa = opa - 256 if (opa & 0x80) else opa
                    sb = opb - 256 if (opb & 0x80) else opb
                    if mode == 1:
                        val = sa - sb
                        if (sa >= 0 and sb < 0 and val > 127) or (sa < 0 and sb >= 0 and val < -128):
                            ovf = 1
                        else:
                            ovf = 0
                    else:
                        val = sa + sb
                        if (sa >= 0 and sb >= 0 and val > 127) or (sa < 0 and sb < 0 and val < -128):
                            ovf = 1
                        else:
                            ovf = 0
                    res = val & 0xFF
                    st = 3
                elif st == 3:
                    st = 0

        row_idx += 1

    return out
