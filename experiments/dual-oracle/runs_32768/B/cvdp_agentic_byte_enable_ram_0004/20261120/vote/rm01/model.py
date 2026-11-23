def reference(vectors):
    LINES = 8192
    ADDR_MASK = LINES - 1
    DATA_MASK = 0xFFFFFFFF
    ram = [0] * LINES
    addr_a_reg = en_a_reg = be_a_reg = data_in_a_reg = 0
    addr_b_reg = en_b_reg = be_b_reg = data_in_b_reg = 0
    data_out_a = data_out_b = 0
    addr_a = en_a = be_a = data_in_a = 0
    addr_b = en_b = be_b = data_in_b = 0
    result = []
    for row in vectors:
        edge = None
        if isinstance(row, dict):
            if 'addr_a' in row: addr_a = int(row['addr_a']) & ADDR_MASK
            if 'en_a' in row: en_a = int(row['en_a']) & 1
            if 'be_a' in row: be_a = int(row['be_a']) & 0xF
            if 'data_in_a' in row: data_in_a = int(row['data_in_a']) & DATA_MASK
            if 'addr_b' in row: addr_b = int(row['addr_b']) & ADDR_MASK
            if 'en_b' in row: en_b = int(row['en_b']) & 1
            if 'be_b' in row: be_b = int(row['be_b']) & 0xF
            if 'data_in_b' in row: data_in_b = int(row['data_in_b']) & DATA_MASK
            edge = row.get('edge', None)
        else:
            if isinstance(row, (list, tuple)) and len(row) >= 9:
                edge = row[0]
                addr_a = int(row[1]) & ADDR_MASK
                en_a = int(row[2]) & 1
                be_a = int(row[3]) & 0xF
                data_in_a = int(row[4]) & DATA_MASK
                addr_b = int(row[5]) & ADDR_MASK
                en_b = int(row[6]) & 1
                be_b = int(row[7]) & 0xF
                data_in_b = int(row[8]) & DATA_MASK
        result.append({'data_out_a': data_out_a & DATA_MASK, 'data_out_b': data_out_b & DATA_MASK})
        pose = False
        if edge is not None:
            if isinstance(edge, str):
                e = edge.lower()
                if e.startswith('pos') or e == 'p' or e == '1':
                    pose = True
            else:
                try:
                    if int(edge) == 1:
                        pose = True
                except:
                    pass
        if pose:
            read_a = ram[addr_a_reg]
            read_b = ram[addr_b_reg]
            addrs = []
            if en_a_reg:
                if addr_a_reg not in addrs:
                    addrs.append(addr_a_reg)
            if en_b_reg:
                if addr_b_reg not in addrs:
                    addrs.append(addr_b_reg)
            for addr in addrs:
                old_word = ram[addr]
                nw = 0
                a_match = en_a_reg and (addr_a_reg == addr)
                b_match = en_b_reg and (addr_b_reg == addr)
                for i in range(4):
                    shift = i * 8
                    old_byte = (old_word >> shift) & 0xFF
                    new_byte = old_byte
                    if a_match and ((be_a_reg >> i) & 1):
                        new_byte = (data_in_a_reg >> shift) & 0xFF
                    elif b_match and ((be_b_reg >> i) & 1):
                        new_byte = (data_in_b_reg >> shift) & 0xFF
                    nw |= (new_byte << shift)
                ram[addr] = nw & DATA_MASK
            data_out_a = read_a & DATA_MASK
            data_out_b = read_b & DATA_MASK
            addr_a_reg = addr_a
            en_a_reg = en_a
            be_a_reg = be_a
            data_in_a_reg = data_in_a
            addr_b_reg = addr_b
            en_b_reg = en_b
            be_b_reg = be_b
            data_in_b_reg = data_in_b
    return result
