def reference(vectors):
    LINES = 8192
    MASK_ADDR = LINES - 1
    MASK_WORD = 0xFFFFFFFF

    ram = [0] * LINES

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

    results = []

    for idx, v in enumerate(vectors):
        def getval(key, default=0):
            if isinstance(v, dict):
                return v.get(key, default)
            return getattr(v, key, default)

        is_pos = None
        if isinstance(v, dict):
            if 'clk' in v:
                c = v['clk']
                if isinstance(c, str):
                    is_pos = c.lower() in ('1', 'posedge', 'rise', 'rising', 'true')
                else:
                    is_pos = bool(c)
            elif 'edge' in v:
                e = v['edge']
                if isinstance(e, str):
                    is_pos = e.lower() in ('posedge', 'rise', 'rising', '1', 'true')
                else:
                    is_pos = bool(e)
            elif 'posedge' in v:
                is_pos = bool(v['posedge'])
        else:
            if hasattr(v, 'clk'):
                c = getattr(v, 'clk')
                if isinstance(c, str):
                    is_pos = c.lower() in ('1', 'posedge', 'rise', 'rising', 'true')
                else:
                    is_pos = bool(c)
            elif hasattr(v, 'edge'):
                e = getattr(v, 'edge')
                if isinstance(e, str):
                    is_pos = e.lower() in ('posedge', 'rise', 'rising', '1', 'true')
                else:
                    is_pos = bool(e)
        if is_pos is None:
            is_pos = (idx % 2 == 0)

        results.append({
            'data_out_a': data_out_a & MASK_WORD,
            'data_out_b': data_out_b & MASK_WORD
        })

        if is_pos:
            read_a = ram[addr_a_reg & MASK_ADDR]
            read_b = ram[addr_b_reg & MASK_ADDR]

            if en_a_reg and en_b_reg and (addr_a_reg == addr_b_reg):
                addr = addr_a_reg & MASK_ADDR
                word = ram[addr]
                for i in range(4):
                    shift = i * 8
                    if (be_a_reg >> i) & 1:
                        val = (data_in_a_reg >> shift) & 0xFF
                        mask = 0xFF << shift
                        word = (word & (MASK_WORD ^ mask)) | (val << shift)
                    elif (be_b_reg >> i) & 1:
                        val = (data_in_b_reg >> shift) & 0xFF
                        mask = 0xFF << shift
                        word = (word & (MASK_WORD ^ mask)) | (val << shift)
                ram[addr] = word & MASK_WORD
            else:
                if en_a_reg:
                    addr = addr_a_reg & MASK_ADDR
                    word = ram[addr]
                    for i in range(4):
                        if (be_a_reg >> i) & 1:
                            shift = i * 8
                            val = (data_in_a_reg >> shift) & 0xFF
                            mask = 0xFF << shift
                            word = (word & (MASK_WORD ^ mask)) | (val << shift)
                    ram[addr] = word & MASK_WORD
                if en_b_reg:
                    addr = addr_b_reg & MASK_ADDR
                    word = ram[addr]
                    for i in range(4):
                        if (be_b_reg >> i) & 1:
                            shift = i * 8
                            val = (data_in_b_reg >> shift) & 0xFF
                            mask = 0xFF << shift
                            word = (word & (MASK_WORD ^ mask)) | (val << shift)
                    ram[addr] = word & MASK_WORD

            addr_a_reg = getval('addr_a', 0) & MASK_ADDR
            en_a_reg = getval('en_a', 0) & 1
            be_a_reg = getval('be_a', 0) & 0xF
            data_in_a_reg = getval('data_in_a', 0) & MASK_WORD

            addr_b_reg = getval('addr_b', 0) & MASK_ADDR
            en_b_reg = getval('en_b', 0) & 1
            be_b_reg = getval('be_b', 0) & 0xF
            data_in_b_reg = getval('data_in_b', 0) & MASK_WORD

            data_out_a = read_a & MASK_WORD
            data_out_b = read_b & MASK_WORD

    return results
