def reference(vectors):
    def get(row, name, default=0):
        if isinstance(row, dict):
            if name in row:
                return row[name]
            if name.startswith('i_') and name[2:] in row:
                return row[name[2:]]
            lname = name.lower()
            for k in row:
                if isinstance(k, str) and k.lower() == lname:
                    return row[k]
            return default
        if hasattr(row, name):
            return getattr(row, name)
        if name.startswith('i_') and hasattr(row, name[2:]):
            return getattr(row, name[2:])
        return default

    def as_int(x, default=0):
        if x is None:
            return default
        if isinstance(x, bool):
            return 1 if x else 0
        if isinstance(x, int):
            return x
        if isinstance(x, str):
            s = x.strip().lower()
            if s in ('true', 'high', '1'):
                return 1
            if s in ('false', 'low', '0'):
                return 0
            try:
                return int(s, 0)
            except:
                return default
        return default

    def edge_is_pos(row):
        e = get(row, 'edge', None)
        if e is None:
            clk = get(row, 'i_clk', None)
            if clk is not None:
                return as_int(clk, 0) != 0
            return True
        if isinstance(e, str):
            s = e.strip().lower()
            if 'pos' in s or 'ris' in s or 'rise' in s:
                return True
            if 'neg' in s or 'fall' in s:
                return False
            if s in ('1', 'true', 'high'):
                return True
            if s in ('0', 'false', 'low'):
                return False
            return True
        if isinstance(e, bool):
            return e
        if isinstance(e, int):
            return e != 0
        return True

    if isinstance(vectors, dict):
        if 'vectors' in vectors:
            vectors = vectors['vectors']
        elif any(k in vectors for k in ('edge', 'i_rst_n', 'i_clk', 'i_enable')):
            vectors = [vectors]

    IDLE, LOAD, COMPUTE, OUTPUT = 0, 1, 2, 3
    state = IDLE
    a_reg = 0
    b_reg = 0
    result = 0
    overflow = 0
    out_rows = []

    for row in vectors:
        rst = as_int(get(row, 'i_rst_n', 1), 1)
        clear = as_int(get(row, 'i_clear', 0), 0)
        start = as_int(get(row, 'i_start', 0), 0)
        enable = as_int(get(row, 'i_enable', 0), 0)
        mode = as_int(get(row, 'i_mode', 0), 0)
        a_in = as_int(get(row, 'i_operand_a', 0), 0) & 0xFF
        b_in = as_int(get(row, 'i_operand_b', 0), 0) & 0xFF
        pos = edge_is_pos(row)

        if rst == 0:
            state = IDLE
            a_reg = 0
            b_reg = 0
            result = 0
            overflow = 0

        out_rows.append({
            'o_resultant_sum': result & 0xFF,
            'o_overflow': overflow & 1,
            'o_ready': 1 if state == OUTPUT else 0,
            'o_status': state & 3
        })

        if pos and rst != 0:
            if clear != 0:
                state = IDLE
                a_reg = 0
                b_reg = 0
                result = 0
                overflow = 0
            elif enable == 0:
                state = IDLE
            else:
                if state == IDLE:
                    if start != 0:
                        state = LOAD
                elif state == LOAD:
                    a_reg = a_in
                    b_reg = b_in
                    state = COMPUTE
                elif state == COMPUTE:
                    if mode & 1:
                        res = (a_reg - b_reg) & 0xFF
                        sa = (a_reg >> 7) & 1
                        sb = (b_reg >> 7) & 1
                        sr = (res >> 7) & 1
                        overflow = 1 if (sa != sb and sr != sa) else 0
                    else:
                        res = (a_reg + b_reg) & 0xFF
                        sa = (a_reg >> 7) & 1
                        sb = (b_reg >> 7) & 1
                        sr = (res >> 7) & 1
                        overflow = 1 if (sa == sb and sr != sa) else 0
                    result = res
                    state = OUTPUT
                elif state == OUTPUT:
                    state = IDLE

    return out_rows
