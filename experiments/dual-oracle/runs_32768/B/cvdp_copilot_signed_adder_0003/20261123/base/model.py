def reference(vectors):
    IDLE, LOAD, COMPUTE, OUTPUT = 0, 1, 2, 3
    state = IDLE
    result = 0
    overflow = 0
    a_reg = 0
    b_reg = 0
    out = []

    for idx, row in enumerate(vectors):
        if isinstance(row, dict) and "edge" in row:
            e = row["edge"]
            if isinstance(e, str):
                posedge = e.lower().startswith("pos")
            else:
                posedge = bool(e)
        elif isinstance(row, dict) and "i_clk" in row:
            posedge = (int(row.get("i_clk", 0)) & 1) == 1
        else:
            posedge = (idx % 2 == 0)

        rst_n = int(row.get("i_rst_n", 1)) & 1
        clear = int(row.get("i_clear", 0)) & 1
        enable = int(row.get("i_enable", 0)) & 1
        start = int(row.get("i_start", 0)) & 1
        mode = int(row.get("i_mode", 0)) & 1
        op_a = int(row.get("i_operand_a", 0)) & 0xFF
        op_b = int(row.get("i_operand_b", 0)) & 0xFF

        if rst_n == 0:
            state = IDLE
            result = 0
            overflow = 0
            a_reg = 0
            b_reg = 0
        elif clear == 1:
            state = IDLE
            result = 0
            overflow = 0

        out.append({
            "o_resultant_sum": result & 0xFF,
            "o_overflow": overflow & 1,
            "o_ready": 1 if state == OUTPUT else 0,
            "o_status": state & 3
        })

        if posedge:
            if rst_n == 0:
                state = IDLE
                result = 0
                overflow = 0
                a_reg = 0
                b_reg = 0
            elif clear == 1:
                state = IDLE
                result = 0
                overflow = 0
            else:
                if state == IDLE:
                    if enable and start:
                        state = LOAD
                elif state == LOAD:
                    a_reg = op_a
                    b_reg = op_b
                    state = COMPUTE
                elif state == COMPUTE:
                    sa = a_reg if a_reg < 128 else a_reg - 256
                    sb = b_reg if b_reg < 128 else b_reg - 256
                    if mode:
                        exact = sa - sb
                    else:
                        exact = sa + sb
                    overflow = 1 if (exact < -128 or exact > 127) else 0
                    result = exact & 0xFF
                    state = OUTPUT
                elif state == OUTPUT:
                    state = IDLE

    return out
