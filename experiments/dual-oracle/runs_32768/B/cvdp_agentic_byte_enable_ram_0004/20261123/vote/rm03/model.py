def reference(vectors):
    ram = [0] * 8192
    s_addr_a = s_en_a = s_be_a = s_data_a = 0
    s_addr_b = s_en_b = s_be_b = s_data_b = 0
    dout_a = dout_b = 0
    out = []
    for idx, row in enumerate(vectors):
        edge = None
        clk = None
        if isinstance(row, dict):
            edge = row.get('edge', None)
            clk = row.get('clk', None)
            addr_a = row.get('addr_a', 0)
            en_a = row.get('en_a', 0)
            be_a = row.get('be_a', 0)
            data_in_a = row.get('data_in_a', 0)
            addr_b = row.get('addr_b', 0)
            en_b = row.get('en_b', 0)
            be_b = row.get('be_b', 0)
            data_in_b = row.get('data_in_b', 0)
        else:
            vals = list(row)
            if vals and isinstance(vals[0], str):
                edge = vals[0]
                vals = vals[1:]
            if vals and isinstance(vals[-1], str):
                edge = vals[-1]
                vals = vals[:-1]
            if len(vals) >= 9:
                if isinstance(vals[-1], int) and vals[-1] in (0, 1) and not (isinstance(vals[0], int) and vals[0] in (0, 1)):
                    clk = vals[-1]
                    vals = vals[:-1]
                elif isinstance(vals[0], int) and vals[0] in (0, 1):
                    clk = vals[0]
                    vals = vals[1:]
            vals = vals + [0] * 8
            addr_a, en_a, be_a, data_in_a, addr_b, en_b, be_b, data_in_b = vals[:8]
        if edge is not None:
            if isinstance(edge, str):
                is_pos = edge.lower().startswith('pos')
            else:
                is_pos = bool(edge)
        elif clk is not None:
            is_pos = (clk == 1 or clk is True)
        else:
            is_pos = (idx % 2 == 0)
        out.append({'data_out_a': dout_a & 0xFFFFFFFF, 'data_out_b': dout_b & 0xFFFFFFFF})
        if not is_pos:
            continue
        ndout_a = ram[s_addr_a] & 0xFFFFFFFF
        ndout_b = ram[s_addr_b] & 0xFFFFFFFF
        if s_en_a and s_en_b and (s_addr_a == s_addr_b):
            addr = s_addr_a
            neww = ram[addr]
            if s_be_a & 1:
                neww = (neww & ~0xFF) | (s_data_a & 0xFF)
            elif s_be_b & 1:
                neww = (neww & ~0xFF) | (s_data_b & 0xFF)
            if s_be_a & 2:
                neww = (neww & ~0xFF00) | (((s_data_a >> 8) & 0xFF) << 8)
            elif s_be_b & 2:
                neww = (neww & ~0xFF00) | (((s_data_b >> 8) & 0xFF) << 8)
            if s_be_a & 4:
                neww = (neww & ~0xFF0000) | (((s_data_a >> 16) & 0xFF) << 16)
            elif s_be_b & 4:
                neww = (neww & ~0xFF0000) | (((s_data_b >> 16) & 0xFF) << 16)
            if s_be_a & 8:
                neww = (neww & ~0xFF000000) | (((s_data_a >> 24) & 0xFF) << 24)
            elif s_be_b & 8:
                neww = (neww & ~0xFF000000) | (((s_data_b >> 24) & 0xFF) << 24)
            ram[addr] = neww & 0xFFFFFFFF
        else:
            if s_en_a:
                addr = s_addr_a
                neww = ram[addr]
                if s_be_a & 1:
                    neww = (neww & ~0xFF) | (s_data_a & 0xFF)
                if s_be_a & 2:
                    neww = (neww & ~0xFF00) | (((s_data_a >> 8) & 0xFF) << 8)
                if s_be_a & 4:
                    neww = (neww & ~0xFF0000) | (((s_data_a >> 16) & 0xFF) << 16)
                if s_be_a & 8:
                    neww = (neww & ~0xFF000000) | (((s_data_a >> 24) & 0xFF) << 24)
                ram[addr] = neww & 0xFFFFFFFF
            if s_en_b:
                addr = s_addr_b
                neww = ram[addr]
                if s_be_b & 1:
                    neww = (neww & ~0xFF) | (s_data_b & 0xFF)
                if s_be_b & 2:
                    neww = (neww & ~0xFF00) | (((s_data_b >> 8) & 0xFF) << 8)
                if s_be_b & 4:
                    neww = (neww & ~0xFF0000) | (((s_data_b >> 16) & 0xFF) << 16)
                if s_be_b & 8:
                    neww = (neww & ~0xFF000000) | (((s_data_b >> 24) & 0xFF) << 24)
                ram[addr] = neww & 0xFFFFFFFF
        s_addr_a = addr_a & 0x1FFF
        s_en_a = 1 if en_a else 0
        s_be_a = be_a & 0xF
        s_data_a = data_in_a & 0xFFFFFFFF
        s_addr_b = addr_b & 0x1FFF
        s_en_b = 1 if en_b else 0
        s_be_b = be_b & 0xF
        s_data_b = data_in_b & 0xFFFFFFFF
        dout_a = ndout_a
        dout_b = ndout_b
    return out
