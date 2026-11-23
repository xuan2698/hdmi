def reference(vectors):
    if isinstance(vectors, dict):
        if 'vectors' in vectors:
            vectors = vectors['vectors']
        elif 'rows' in vectors:
            vectors = vectors['rows']
    M32 = 0xffffffff
    cur = {'addr_a':0,'en_a':0,'be_a':0,'data_in_a':0,
           'addr_b':0,'en_b':0,'be_b':0,'data_in_b':0}
    a_addr = a_en = a_be = a_data = 0
    b_addr = b_en = b_be = b_data = 0
    out_a = out_b = 0
    ram = {}
    res = []
    for idx, row in enumerate(vectors):
        edge = None
        if isinstance(row, dict):
            for k in cur:
                if k in row:
                    v = row[k]
                    if isinstance(v, str):
                        v = int(v, 0)
                    else:
                        v = int(v)
                    if k.startswith('addr'):
                        cur[k] = v & 0x1fff
                    elif k.startswith('en'):
                        cur[k] = v & 1
                    elif k.startswith('be'):
                        cur[k] = v & 0xf
                    else:
                        cur[k] = v & M32
            if 'edge' in row:
                edge = row['edge']
            elif 'clk' in row:
                edge = row['clk']
            elif 'clock' in row:
                edge = row['clock']
            elif 'CLK' in row:
                edge = row['CLK']
        else:
            if isinstance(row, (list, tuple)) and len(row) > 0:
                edge = row[0]
        if edge is None:
            is_pos = (idx % 2 == 0)
        elif isinstance(edge, str):
            s = edge.lower()
            if 'pos' in s or 'rise' in s or 'up' in s:
                is_pos = True
            elif 'neg' in s or 'fall' in s or 'down' in s:
                is_pos = False
            else:
                is_pos = (idx % 2 == 0)
        elif isinstance(edge, bool):
            is_pos = edge
        elif isinstance(edge, (int, float)):
            is_pos = (int(edge) != 0)
        else:
            is_pos = (idx % 2 == 0)
        res.append({'data_out_a': out_a & M32, 'data_out_b': out_b & M32})
        if is_pos:
            new_out_a = ram.get(a_addr, 0) & M32
            new_out_b = ram.get(b_addr, 0) & M32
            if a_en and b_en and a_addr == b_addr:
                old = ram.get(a_addr, 0) & M32
                new = old
                bea = a_be & 0xf
                beb = b_be & 0xf
                if bea & 1:
                    new = (new & 0xffffff00) | (a_data & 0xff)
                elif beb & 1:
                    new = (new & 0xffffff00) | (b_data & 0xff)
                if bea & 2:
                    new = (new & 0xffff00ff) | (a_data & 0xff00)
                elif beb & 2:
                    new = (new & 0xffff00ff) | (b_data & 0xff00)
                if bea & 4:
                    new = (new & 0xff00ffff) | (a_data & 0xff0000)
                elif beb & 4:
                    new = (new & 0xff00ffff) | (b_data & 0xff0000)
                if bea & 8:
                    new = (new & 0x00ffffff) | (a_data & 0xff000000)
                elif beb & 8:
                    new = (new & 0x00ffffff) | (b_data & 0xff000000)
                ram[a_addr] = new & M32
            else:
                if a_en:
                    old = ram.get(a_addr, 0) & M32
                    new = old
                    bea = a_be & 0xf
                    if bea & 1:
                        new = (new & 0xffffff00) | (a_data & 0xff)
                    if bea & 2:
                        new = (new & 0xffff00ff) | (a_data & 0xff00)
                    if bea & 4:
                        new = (new & 0xff00ffff) | (a_data & 0xff0000)
                    if bea & 8:
                        new = (new & 0x00ffffff) | (a_data & 0xff000000)
                    ram[a_addr] = new & M32
                if b_en:
                    old = ram.get(b_addr, 0) & M32
                    new = old
                    beb = b_be & 0xf
                    if beb & 1:
                        new = (new & 0xffffff00) | (b_data & 0xff)
                    if beb & 2:
                        new = (new & 0xffff00ff) | (b_data & 0xff00)
                    if beb & 4:
                        new = (new & 0xff00ffff) | (b_data & 0xff0000)
                    if beb & 8:
                        new = (new & 0x00ffffff) | (b_data & 0xff000000)
                    ram[b_addr] = new & M32
            out_a = new_out_a
            out_b = new_out_b
            a_addr = cur['addr_a'] & 0x1fff
            a_en = cur['en_a'] & 1
            a_be = cur['be_a'] & 0xf
            a_data = cur['data_in_a'] & M32
            b_addr = cur['addr_b'] & 0x1fff
            b_en = cur['en_b'] & 1
            b_be = cur['be_b'] & 0xf
            b_data = cur['data_in_b'] & M32
    return res
