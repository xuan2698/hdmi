def reference(vectors):
    MASK = (1 << 32) - 1
    ADDR_MASK = (1 << 13) - 1
    BYTE_MASK = 0xFF

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

    result = []

    for row in vectors:
        if isinstance(row, dict):
            edge = row.get("edge", row.get("clk", 0))
        else:
            try:
                edge = row["edge"]
            except Exception:
                edge = 0

        is_pos = False
        if edge == 1 or edge is True:
            is_pos = True
        elif isinstance(edge, str):
            s = edge.lower()
            is_pos = s.startswith("pos") or s == "1"

        result.append({
            "data_out_a": data_out_a & MASK,
            "data_out_b": data_out_b & MASK
        })

        if is_pos:
            if isinstance(row, dict):
                addr_a = row.get("addr_a", 0)
                en_a = row.get("en_a", 0)
                be_a = row.get("be_a", 0)
                data_in_a = row.get("data_in_a", 0)

                addr_b = row.get("addr_b", 0)
                en_b = row.get("en_b", 0)
                be_b = row.get("be_b", 0)
                data_in_b = row.get("data_in_b", 0)
            else:
                addr_a = en_a = be_a = data_in_a = 0
                addr_b = en_b = be_b = data_in_b = 0

            addr_a = int(addr_a) & ADDR_MASK
            en_a = int(en_a) & 1
            be_a = int(be_a) & 0xF
            data_in_a = int(data_in_a) & MASK

            addr_b = int(addr_b) & ADDR_MASK
            en_b = int(en_b) & 1
            be_b = int(be_b) & 0xF
            data_in_b = int(data_in_b) & MASK

            new_out_a = ram[addr_a_reg] & MASK
            new_out_b = ram[addr_b_reg] & MASK

            if en_a_reg and en_b_reg and addr_a_reg == addr_b_reg:
                word = ram[addr_a_reg]

                for i in range(4):
                    bit = 1 << i
                    shift = i * 8

                    if be_a_reg & bit:
                        word = (word & ~(BYTE_MASK << shift)) | (((data_in_a_reg >> shift) & BYTE_MASK) << shift)
                    elif be_b_reg & bit:
                        word = (word & ~(BYTE_MASK << shift)) | (((data_in_b_reg >> shift) & BYTE_MASK) << shift)

                ram[addr_a_reg] = word & MASK
            else:
                if en_a_reg:
                    word = ram[addr_a_reg]

                    for i in range(4):
                        if be_a_reg & (1 << i):
                            shift = i * 8
                            word = (word & ~(BYTE_MASK << shift)) | (((data_in_a_reg >> shift) & BYTE_MASK) << shift)

                    ram[addr_a_reg] = word & MASK

                if en_b_reg:
                    word = ram[addr_b_reg]

                    for i in range(4):
                        if be_b_reg & (1 << i):
                            shift = i * 8
                            word = (word & ~(BYTE_MASK << shift)) | (((data_in_b_reg >> shift) & BYTE_MASK) << shift)

                    ram[addr_b_reg] = word & MASK

            addr_a_reg = addr_a
            en_a_reg = en_a
            be_a_reg = be_a
            data_in_a_reg = data_in_a

            addr_b_reg = addr_b
            en_b_reg = en_b
            be_b_reg = be_b
            data_in_b_reg = data_in_b

            data_out_a = new_out_a
            data_out_b = new_out_b

    return result
