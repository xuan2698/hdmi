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
    current = {
        'addr_a': 0, 'en_a': 0, 'be_a': 0, 'data_in_a': 0,
        'addr_b': 0, 'en_b': 0, 'be_b': 0, 'data_in_b': 0
    }
    res = []
    for idx, row in enumerate(vectors):
        res.append({'data_out_a': data_out_a & 0xFFFFFFFF,
                    'data_out_b': data_out_b & 0xFFFFFFFF})
        for k in current:
            if k in row:
                current[k] = row[k]
        is_pos = False
        if 'edge' in row:
            e = row['edge']
            if isinstance(e, str):
                is_pos = e.lower().startswith('pos') or e == '1'
            else:
                is_pos = bool(e)
        elif 'clk' in row:
            c = row['clk']
            if isinstance(c, str):
                is_pos = c.lower().startswith('pos') or c == '1'
            else:
                is_pos = (c == 1)
        else:
            is_pos = (idx % 2 == 0)
        if is_pos:
            new_addr_a = current['addr_a'] & 0x1FFF
            new_en_a = current['en_a'] & 1
            new_be_a = current['be_a'] & 0xF
            new_data_in_a = current['data_in_a'] & 0xFFFFFFFF
            new_addr_b = current['addr_b'] & 0x1FFF
            new_en_b = current['en_b'] & 1
            new_be_b = current['be_b'] & 0xF
            new_data_in_b = current['data_in_b'] & 0xFFFFFFFF
            read_a = ram[addr_a_reg] & 0xFFFFFFFF
            read_b = ram[addr_b_reg] & 0xFFFFFFFF
            if en_a_reg and en_b_reg and (addr_a_reg == addr_b_reg):
                old_word = ram[addr_a_reg]
                new_word = 0
                for i in range(4):
                    shift = 8 * i
                    if (be_a_reg >> i) & 1:
                        byte = (data_in_a_reg >> shift) & 0xFF
                    elif (be_b_reg >> i) & 1:
                        byte = (data_in_b_reg >> shift) & 0xFF
                    else:
                        byte = (old_word >> shift) & 0xFF
                    new_word |= byte << shift
                ram[addr_a_reg] = new_word & 0xFFFFFFFF
            else:
                if en_a_reg:
                    old_word = ram[addr_a_reg]
                    new_word = old_word
                    for i in range(4):
                        if (be_a_reg >> i) & 1:
                            shift = 8 * i
                            byte = (data_in_a_reg >> shift) & 0xFF
                            mask = 0xFF << shift
                            new_word = (new_word & ~mask) | (byte << shift)
                    ram[addr_a_reg] = new_word & 0xFFFFFFFF
                if en_b_reg:
                    old_word = ram[addr_b_reg]
                    new_word = old_word
                    for i in range(4):
                        if (be_b_reg >> i) & 1:
                            shift = 8 * i
                            byte = (data_in_b_reg >> shift) & 0xFF
                            mask = 0xFF << shift
                            new_word = (new_word & ~mask) | (byte << shift)
                    ram[addr_b_reg] = new_word & 0xFFFFFFFF
            data_out_a = read_a & 0xFFFFFFFF
            data_out_b = read_b & 0xFFFFFFFF
            addr_a_reg = new_addr_a
            en_a_reg = new_en_a
            be_a_reg = new_be_a
            data_in_a_reg = new_data_in_a
            addr_b_reg = new_addr_b
            en_b_reg = new_en_b
            be_b_reg = new_be_b
            data_in_b_reg = new_data_in_b
    return res
