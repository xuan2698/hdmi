def reference(vectors):
    LINES = 8192
    ram = [0] * LINES
    addr_a_reg = en_a_reg = be_a_reg = data_in_a_reg = 0
    addr_b_reg = en_b_reg = be_b_reg = data_in_b_reg = 0
    data_out_a = data_out_b = 0
    addr_a = en_a = be_a = data_in_a = 0
    addr_b = en_b = be_b = data_in_b = 0
    res = []
    for idx, row in enumerate(vectors):
        if 'addr_a' in row: addr_a = row['addr_a'] & 0x1FFF
        if 'en_a' in row: en_a = row['en_a'] & 1
        if 'be_a' in row: be_a = row['be_a'] & 0xF
        if 'data_in_a' in row: data_in_a = row['data_in_a'] & 0xFFFFFFFF
        if 'addr_b' in row: addr_b = row['addr_b'] & 0x1FFF
        if 'en_b' in row: en_b = row['en_b'] & 1
        if 'be_b' in row: be_b = row['be_b'] & 0xF
        if 'data_in_b' in row: data_in_b = row['data_in_b'] & 0xFFFFFFFF

        posedge = None
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                posedge = 'pos' in e.lower()
            else:
                posedge = (e == 1 or e == True or e == '1')
        elif 'clk' in row:
            c = row['clk']
            posedge = (c == 1 or c == True or c == '1')
        else:
            posedge = (idx % 2 == 0)

        if posedge:
            out_a, out_b = data_out_a, data_out_b
            next_out_a = ram[addr_a_reg]
            next_out_b = ram[addr_b_reg]

            if en_a_reg and en_b_reg and (addr_a_reg == addr_b_reg):
                addr = addr_a_reg
                word = ram[addr]
                for i in range(4):
                    shift = i * 8
                    mask = 0xFF << shift
                    if be_a_reg & (1 << i):
                        byte = (data_in_a_reg >> shift) & 0xFF
                        word = (word & ~mask) | (byte << shift)
                    elif be_b_reg & (1 << i):
                        byte = (data_in_b_reg >> shift) & 0xFF
                        word = (word & ~mask) | (byte << shift)
                ram[addr] = word & 0xFFFFFFFF
            else:
                if en_a_reg:
                    addr = addr_a_reg
                    word = ram[addr]
                    for i in range(4):
                        if be_a_reg & (1 << i):
                            shift = i * 8
                            byte = (data_in_a_reg >> shift) & 0xFF
                            mask = 0xFF << shift
                            word = (word & ~mask) | (byte << shift)
                    ram[addr] = word & 0xFFFFFFFF
                if en_b_reg:
                    addr = addr_b_reg
                    word = ram[addr]
                    for i in range(4):
                        if be_b_reg & (1 << i):
                            shift = i * 8
                            byte = (data_in_b_reg >> shift) & 0xFF
                            mask = 0xFF << shift
                            word = (word & ~mask) | (byte << shift)
                    ram[addr] = word & 0xFFFFFFFF

            addr_a_reg, en_a_reg, be_a_reg, data_in_a_reg = addr_a, en_a, be_a, data_in_a
            addr_b_reg, en_b_reg, be_b_reg, data_in_b_reg = addr_b, en_b, be_b, data_in_b
            data_out_a = next_out_a & 0xFFFFFFFF
            data_out_b = next_out_b & 0xFFFFFFFF
            res.append({'data_out_a': out_a, 'data_out_b': out_b})
        else:
            res.append({'data_out_a': data_out_a, 'data_out_b': data_out_b})
    return res
