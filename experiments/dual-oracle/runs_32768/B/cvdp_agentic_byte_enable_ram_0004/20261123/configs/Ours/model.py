def reference(vectors):
    MASK32 = (1 << 32) - 1
    LINES = 8192
    ADDR_MASK = LINES - 1
    ram = [0] * LINES

    s_addr_a = 0
    s_en_a = 0
    s_be_a = 0
    s_data_a = 0
    s_addr_b = 0
    s_en_b = 0
    s_be_b = 0
    s_data_b = 0

    out_a = 0
    out_b = 0

    in_addr_a = 0
    in_en_a = 0
    in_be_a = 0
    in_data_a = 0
    in_addr_b = 0
    in_en_b = 0
    in_be_b = 0
    in_data_b = 0

    results = []

    for idx, row in enumerate(vectors):
        if isinstance(row, dict):
            if 'addr_a' in row:
                in_addr_a = int(row['addr_a']) & ADDR_MASK
            if 'en_a' in row:
                in_en_a = int(row['en_a']) & 1
            if 'be_a' in row:
                in_be_a = int(row['be_a']) & 0xF
            if 'data_in_a' in row:
                in_data_a = int(row['data_in_a']) & MASK32
            if 'addr_b' in row:
                in_addr_b = int(row['addr_b']) & ADDR_MASK
            if 'en_b' in row:
                in_en_b = int(row['en_b']) & 1
            if 'be_b' in row:
                in_be_b = int(row['be_b']) & 0xF
            if 'data_in_b' in row:
                in_data_b = int(row['data_in_b']) & MASK32
            ev = row.get('edge', None)
            if ev is None:
                ev = row.get('clk', None)
        else:
            ev = None

        if ev is None:
            pos = (idx % 2 == 0)
        elif isinstance(ev, str):
            s = ev.lower()
            if 'pos' in s or 'rise' in s or s == '1' or s == 'p':
                pos = True
            elif 'neg' in s or 'fall' in s or s == '0' or s == 'n':
                pos = False
            else:
                pos = (idx % 2 == 0)
        else:
            pos = bool(int(ev))

        results.append({
            'data_out_a': out_a & MASK32,
            'data_out_b': out_b & MASK32
        })

        if pos:
            new_out_a = ram[s_addr_a]
            new_out_b = ram[s_addr_b]

            if s_en_a and s_en_b and s_addr_a == s_addr_b:
                addr = s_addr_a
                neww = ram[addr]
                for i in range(4):
                    bit = 1 << i
                    if s_be_a & bit:
                        b = (s_data_a >> (8 * i)) & 0xFF
                    elif s_be_b & bit:
                        b = (s_data_b >> (8 * i)) & 0xFF
                    else:
                        continue
                    mask = 0xFF << (8 * i)
                    neww = (neww & ~mask) | (b << (8 * i))
                ram[addr] = neww & MASK32
            else:
                if s_en_a:
                    addr = s_addr_a
                    neww = ram[addr]
                    for i in range(4):
                        if (s_be_a >> i) & 1:
                            b = (s_data_a >> (8 * i)) & 0xFF
                            mask = 0xFF << (8 * i)
                            neww = (neww & ~mask) | (b << (8 * i))
                    ram[addr] = neww & MASK32
                if s_en_b:
                    addr = s_addr_b
                    neww = ram[addr]
                    for i in range(4):
                        if (s_be_b >> i) & 1:
                            b = (s_data_b >> (8 * i)) & 0xFF
                            mask = 0xFF << (8 * i)
                            neww = (neww & ~mask) | (b << (8 * i))
                    ram[addr] = neww & MASK32

            s_addr_a = in_addr_a
            s_en_a = in_en_a
            s_be_a = in_be_a
            s_data_a = in_data_a
            s_addr_b = in_addr_b
            s_en_b = in_en_b
            s_be_b = in_be_b
            s_data_b = in_data_b

            out_a = new_out_a & MASK32
            out_b = new_out_b & MASK32

    return results
