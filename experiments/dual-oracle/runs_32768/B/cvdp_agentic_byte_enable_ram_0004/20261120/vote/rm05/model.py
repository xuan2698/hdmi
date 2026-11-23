def reference(vectors):
    LINES = 8192
    MASK32 = 0xFFFFFFFF
    ram = [0] * LINES
    a_addr = 0
    a_en = 0
    a_be = 0
    a_data = 0
    b_addr = 0
    b_en = 0
    b_be = 0
    b_data = 0
    out_a = 0
    out_b = 0
    res = []
    for idx, row in enumerate(vectors):
        clk = None
        if isinstance(row, dict):
            addr_a = int(row.get('addr_a', 0))
            en_a = int(row.get('en_a', 0))
            be_a = int(row.get('be_a', 0))
            data_in_a = int(row.get('data_in_a', 0))
            addr_b = int(row.get('addr_b', 0))
            en_b = int(row.get('en_b', 0))
            be_b = int(row.get('be_b', 0))
            data_in_b = int(row.get('data_in_b', 0))
            if 'clk' in row:
                clk = int(row['clk'])
        else:
            try:
                addr_a = int(row.addr_a)
                en_a = int(row.en_a)
                be_a = int(row.be_a)
                data_in_a = int(row.data_in_a)
                addr_b = int(row.addr_b)
                en_b = int(row.en_b)
                be_b = int(row.be_b)
                data_in_b = int(row.data_in_b)
                clk = int(row.clk) if hasattr(row, 'clk') else None
            except Exception:
                try:
                    L = len(row)
                except Exception:
                    L = 0
                if L == 9:
                    clk = int(row[0])
                    addr_a = int(row[1])
                    en_a = int(row[2])
                    be_a = int(row[3])
                    data_in_a = int(row[4])
                    addr_b = int(row[5])
                    en_b = int(row[6])
                    be_b = int(row[7])
                    data_in_b = int(row[8])
                elif L == 8:
                    clk = None
                    addr_a = int(row[0])
                    en_a = int(row[1])
                    be_a = int(row[2])
                    data_in_a = int(row[3])
                    addr_b = int(row[4])
                    en_b = int(row[5])
                    be_b = int(row[6])
                    data_in_b = int(row[7])
                else:
                    clk = None
                    addr_a = en_a = be_a = data_in_a = addr_b = en_b = be_b = data_in_b = 0
        addr_a &= 0x1FFF
        en_a &= 1
        be_a &= 0xF
        data_in_a &= MASK32
        addr_b &= 0x1FFF
        en_b &= 1
        be_b &= 0xF
        data_in_b &= MASK32
        if clk is None:
            posedge = (idx % 2 == 0)
        else:
            posedge = (clk == 1)
        res.append({'data_out_a': out_a & MASK32, 'data_out_b': out_b & MASK32})
        if not posedge:
            continue
        read_a = ram[a_addr] if a_addr < LINES else 0
        read_b = ram[b_addr] if b_addr < LINES else 0
        if a_en and b_en and (a_addr == b_addr):
            addr = a_addr
            if 0 <= addr < LINES:
                old_word = ram[addr]
                new_word = old_word
                for i in range(4):
                    shift = 8 * i
                    mask = 0xFF << shift
                    if a_be & (1 << i):
                        byte_val = (a_data >> shift) & 0xFF
                        new_word = (new_word & ~mask) | (byte_val << shift)
                    elif b_be & (1 << i):
                        byte_val = (b_data >> shift) & 0xFF
                        new_word = (new_word & ~mask) | (byte_val << shift)
                ram[addr] = new_word & MASK32
        else:
            if a_en and 0 <= a_addr < LINES:
                old_word = ram[a_addr]
                new_word = old_word
                for i in range(4):
                    if a_be & (1 << i):
                        shift = 8 * i
                        mask = 0xFF << shift
                        byte_val = (a_data >> shift) & 0xFF
                        new_word = (new_word & ~mask) | (byte_val << shift)
                ram[a_addr] = new_word & MASK32
            if b_en and 0 <= b_addr < LINES:
                old_word = ram[b_addr]
                new_word = old_word
                for i in range(4):
                    if b_be & (1 << i):
                        shift = 8 * i
                        mask = 0xFF << shift
                        byte_val = (b_data >> shift) & 0xFF
                        new_word = (new_word & ~mask) | (byte_val << shift)
                ram[b_addr] = new_word & MASK32
        a_addr = addr_a
        a_en = en_a
        a_be = be_a
        a_data = data_in_a
        b_addr = addr_b
        b_en = en_b
        b_be = be_b
        b_data = data_in_b
        out_a = read_a & MASK32
        out_b = read_b & MASK32
    return res
