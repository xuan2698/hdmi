def reference(vectors):
    state = 0
    opa = 0
    opb = 0
    res = 0
    ov = 0
    outputs = []

    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            rst = row.get('i_rst_n', 1)
            start = row.get('i_start', 0)
            en = row.get('i_enable', 0)
            mode = row.get('i_mode', 0)
            clear = row.get('i_clear', 0)
            a_in = row.get('i_operand_a', 0) & 255
            b_in = row.get('i_operand_b', 0) & 255
            ev = row.get('edge', None)
            if ev is None and 'i_clk' in row:
                ev = row['i_clk']
        else:
            rst = 1
            start = 0
            en = 0
            mode = 0
            clear = 0
            a_in = 0
            b_in = 0
            ev = None

        if isinstance(ev, str):
            s = ev.lower()
            if 'pos' in s:
                edge = 1
            elif 'neg' in s:
                edge = 0
            else:
                edge = 1 if idx % 2 == 0 else 0
        elif ev is not None:
            edge = 1 if (ev == 1 or ev is True) else 0
        else:
            edge = 1 if idx % 2 == 0 else 0

        if rst == 0:
            state = 0
            opa = 0
            opb = 0
            res = 0
            ov = 0
        elif clear == 1:
            state = 0
            opa = 0
            opb = 0
            res = 0
            ov = 0

        outputs.append({
            'o_resultant_sum': res & 255,
            'o_overflow': ov & 1,
            'o_ready': 1 if state == 3 else 0,
            'o_status': state & 3
        })

        if edge == 1:
            if rst == 0 or clear == 1:
                pass
            else:
                if state == 0:
                    if en == 1 and start == 1:
                        state = 1
                elif state == 1:
                    opa = a_in
                    opb = b_in
                    state = 2
                elif state == 2:
                    sa = opa if opa < 128 else opa - 256
                    sb = opb if opb < 128 else opb - 256
                    if mode == 0:
                        true_res = sa + sb
                        bits = (opa + opb) & 255
                    else:
                        true_res = sa - sb
                        bits = (opa - opb) & 255
                    if true_res < -128 or true_res > 127:
                        ov = 1
                    else:
                        ov = 0
                    res = bits & 255
                    state = 3
                elif state == 3:
                    state = 0

    return outputs
