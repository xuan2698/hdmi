def reference(vectors):
    LINES = 8192
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
    result = []

    for idx, row in enumerate(vectors):
        pos = None
        if isinstance(row, dict):
            if 'edge' in row:
                e = row['edge']
                if isinstance(e, str):
                    el = e.lower()
                    pos = (el == 'posedge' or el == '1' or el == 'true')
                else:
                    pos = (int(e) != 0)
            elif 'clk' in row:
                c = row['clk']
                if isinstance(c, str):
                    cl = c.lower()
                    pos = (cl == '1' or cl == 'posedge' or cl == 'true')
                else:
                    pos = (int(c) != 0)
            elif 'posedge' in row:
                pos = bool(row['posedge'])
        if pos is None:
            pos = (idx % 2 == 0)

        result.append({'data_out_a': out_a & 0xFFFFFFFF, 'data_out_b': out_b & 0xFFFFFFFF})

        if pos:
            old_a_addr = a_addr
            old_b_addr = b_addr
            old_a_en = a_en
            old_b_en = b_en
            old_a_be = a_be
            old_b_be = b_be
            old_a_data = a_data
            old_b_data = b_data

            next_out_a = ram[old_a_addr] if 0 <= old_a_addr < LINES else 0
            next_out_b = ram[old_b_addr] if 0 <= old_b_addr < LINES else 0

            if old_a_en and old_b_en and (old_a_addr == old_b_addr):
                addr = old_a_addr
                if 0 <= addr < LINES:
                    word = ram[addr]
                    for i in range(4):
                        bit = 1 << i
                        shift = 8 * i
                        if old_a_be & bit:
                            byte = (old_a_data >> shift) & 0xFF
                            word = (word & ~(0xFF << shift)) | (byte << shift)
                        elif old_b_be & bit:
                            byte = (old_b_data >> shift) & 0xFF
                            word = (word & ~(0xFF << shift)) | (byte << shift)
                    ram[addr] = word
            else:
                if old_a_en and 0 <= old_a_addr < LINES:
                    addr = old_a_addr
                    word = ram[addr]
                    for i in range(4):
                        bit = 1 << i
                        if old_a_be & bit:
                            shift = 8 * i
                            byte = (old_a_data >> shift) & 0xFF
                            word = (word & ~(0xFF << shift)) | (byte << shift)
                    ram[addr] = word
                if old_b_en and 0 <= old_b_addr < LINES:
                    addr = old_b_addr
                    word = ram[addr]
                    for i in range(4):
                        bit = 1 << i
                        if old_b_be & bit:
                            shift = 8 * i
                            byte = (old_b_data >> shift) & 0xFF
                            word = (word & ~(0xFF << shift)) | (byte << shift)
                    ram[addr] = word

            if isinstance(row, dict):
                a_addr = int(row.get('addr_a', 0)) & 0x1FFF
                a_en = int(row.get('en_a', 0)) & 1
                a_be = int(row.get('be_a', 0)) & 0xF
                a_data = int(row.get('data_in_a', 0)) & 0xFFFFFFFF
                b_addr = int(row.get('addr_b', 0)) & 0x1FFF
                b_en = int(row.get('en_b', 0)) & 1
                b_be = int(row.get('be_b', 0)) & 0xF
                b_data = int(row.get('data_in_b', 0)) & 0xFFFFFFFF
            else:
                a_addr = int(row[0]) & 0x1FFF
                a_en = int(row[1]) & 1
                a_be = int(row[2]) & 0xF
                a_data = int(row[3]) & 0xFFFFFFFF
                b_addr = int(row[4]) & 0x1FFF
                b_en = int(row[5]) & 1
                b_be = int(row[6]) & 0xF
                b_data = int(row[7]) & 0xFFFFFFFF

            out_a = next_out_a & 0xFFFFFFFF
            out_b = next_out_b & 0xFFFFFFFF

    return result
