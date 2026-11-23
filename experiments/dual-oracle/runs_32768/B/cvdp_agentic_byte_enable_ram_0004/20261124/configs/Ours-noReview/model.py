def reference(vectors):
    ram = [0] * 8192
    addr_a_reg = 0
    en_a_reg = 0
    be_a_reg = 0
    data_in_a_reg = 0
    addr_b_reg = 0
    en_b_reg = 0
    be_b_reg = 0
    data_in_b_reg = 0
    data_out_a = 0
    data_out_b = 0
    cur = {
        'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
        'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0
    }
    inputs = list(cur.keys())
    results = []
    for row in vectors:
        for k in inputs:
            if k in row:
                cur[k] = row[k]
        e = row.get('edge', None)
        if e is None:
            pos = bool(row.get('clk', 0))
        elif isinstance(e, str):
            el = e.lower()
            pos = el.startswith('p') or el in ('1', 'true', 'rise', 'rising', 'pos')
        else:
            pos = bool(e)
        results.append({
            'data_out_a': data_out_a & 0xFFFFFFFF,
            'data_out_b': data_out_b & 0xFFFFFFFF
        })
        if not pos:
            continue
        out_a_new = ram[addr_a_reg & 0x1FFF]
        out_b_new = ram[addr_b_reg & 0x1FFF]
        if en_a_reg and en_b_reg and ((addr_a_reg & 0x1FFF) == (addr_b_reg & 0x1FFF)):
            a = addr_a_reg & 0x1FFF
            w = ram[a]
            for i in range(4):
                sh = 8 * i
                m = 0xFF << sh
                if (be_a_reg >> i) & 1:
                    val = (data_in_a_reg >> sh) & 0xFF
                    w = (w & ~m) | (val << sh)
                elif (be_b_reg >> i) & 1:
                    val = (data_in_b_reg >> sh) & 0xFF
                    w = (w & ~m) | (val << sh)
            ram[a] = w & 0xFFFFFFFF
        else:
            if en_a_reg:
                a = addr_a_reg & 0x1FFF
                w = ram[a]
                for i in range(4):
                    if (be_a_reg >> i) & 1:
                        sh = 8 * i
                        m = 0xFF << sh
                        val = (data_in_a_reg >> sh) & 0xFF
                        w = (w & ~m) | (val << sh)
                ram[a] = w & 0xFFFFFFFF
            if en_b_reg:
                a = addr_b_reg & 0x1FFF
                w = ram[a]
                for i in range(4):
                    if (be_b_reg >> i) & 1:
                        sh = 8 * i
                        m = 0xFF << sh
                        val = (data_in_b_reg >> sh) & 0xFF
                        w = (w & ~m) | (val << sh)
                ram[a] = w & 0xFFFFFFFF
        data_out_a = out_a_new & 0xFFFFFFFF
        data_out_b = out_b_new & 0xFFFFFFFF
        addr_a_reg = cur['addr_a'] & 0x1FFF
        en_a_reg = cur['en_a'] & 1
        be_a_reg = cur['be_a'] & 0xF
        data_in_a_reg = cur['data_in_a'] & 0xFFFFFFFF
        addr_b_reg = cur['addr_b'] & 0x1FFF
        en_b_reg = cur['en_b'] & 1
        be_b_reg = cur['be_b'] & 0xF
        data_in_b_reg = cur['data_in_b'] & 0xFFFFFFFF
    return results
