def reference(vectors):
    LINES = 8192
    ram = [0] * LINES
    a_addr = a_en = a_be = a_data = 0
    b_addr = b_en = b_be = b_data = 0
    out_a = out_b = 0
    res = []

    for idx, row in enumerate(vectors):
        is_pos = (idx % 2 == 0)
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    is_pos = ('pos' in e.lower())
                else:
                    is_pos = bool(e)
            elif 'clk' in row:
                is_pos = (row['clk'] != 0)

        sampled_a = out_a
        sampled_b = out_b

        if is_pos:
            if isinstance(row, dict):
                cur_addr_a = row.get('addr_a', 0)
                cur_en_a = row.get('en_a', 0)
                cur_be_a = row.get('be_a', 0)
                cur_data_in_a = row.get('data_in_a', 0)
                cur_addr_b = row.get('addr_b', 0)
                cur_en_b = row.get('en_b', 0)
                cur_be_b = row.get('be_b', 0)
                cur_data_in_b = row.get('data_in_b', 0)
            else:
                cur_addr_a = cur_en_a = cur_be_a = cur_data_in_a = 0
                cur_addr_b = cur_en_b = cur_be_b = cur_data_in_b = 0

            read_a = ram[a_addr & 0x1FFF]
            read_b = ram[b_addr & 0x1FFF]

            writes = {}

            if (a_en & 1) and (b_en & 1) and ((a_addr & 0x1FFF) == (b_addr & 0x1FFF)):
                addr = a_addr & 0x1FFF
                old = ram[addr]
                new = old
                bea = a_be & 0xF
                beb = b_be & 0xF
                da = a_data & 0xFFFFFFFF
                db = b_data & 0xFFFFFFFF
                for i in range(4):
                    mask = 0xFF << (8 * i)
                    if (bea >> i) & 1:
                        byte = (da >> (8 * i)) & 0xFF
                        new = (new & ~mask) | (byte << (8 * i))
                    elif (beb >> i) & 1:
                        byte = (db >> (8 * i)) & 0xFF
                        new = (new & ~mask) | (byte << (8 * i))
                writes[addr] = new & 0xFFFFFFFF
            else:
                if a_en & 1:
                    addr = a_addr & 0x1FFF
                    old = ram[addr]
                    new = old
                    bea = a_be & 0xF
                    da = a_data & 0xFFFFFFFF
                    for i in range(4):
                        if (bea >> i) & 1:
                            mask = 0xFF << (8 * i)
                            byte = (da >> (8 * i)) & 0xFF
                            new = (new & ~mask) | (byte << (8 * i))
                    writes[addr] = new & 0xFFFFFFFF
                if b_en & 1:
                    addr = b_addr & 0x1FFF
                    old = ram[addr]
                    new = old
                    beb = b_be & 0xF
                    db = b_data & 0xFFFFFFFF
                    for i in range(4):
                        if (beb >> i) & 1:
                            mask = 0xFF << (8 * i)
                            byte = (db >> (8 * i)) & 0xFF
                            new = (new & ~mask) | (byte << (8 * i))
                    writes[addr] = new & 0xFFFFFFFF

            for addr, val in writes.items():
                ram[addr] = val & 0xFFFFFFFF

            out_a = read_a & 0xFFFFFFFF
            out_b = read_b & 0xFFFFFFFF

            a_addr = cur_addr_a & 0x1FFF
            a_en = cur_en_a & 1
            a_be = cur_be_a & 0xF
            a_data = cur_data_in_a & 0xFFFFFFFF
            b_addr = cur_addr_b & 0x1FFF
            b_en = cur_en_b & 1
            b_be = cur_be_b & 0xF
            b_data = cur_data_in_b & 0xFFFFFFFF

        res.append({'data_out_a': sampled_a & 0xFFFFFFFF,
                    'data_out_b': sampled_b & 0xFFFFFFFF})

    return res
