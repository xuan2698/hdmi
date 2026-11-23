def reference(vectors):
    def s(v):
        v = int(v) & 0xFFFF
        return v - 0x10000 if v & 0x8000 else v
    o1 = o2 = o3 = 0
    res = []
    for row in vectors:
        rst = row.get('reset', 0)
        if rst:
            o1 = o2 = o3 = 0
        res.append({
            'out_1': o1 & 0xFFFF,
            'out_2': o2 & 0xFFFF,
            'out_3': o3 & 0xFFFF
        })
        edge = row.get('edge')
        if edge is None:
            pos = (row.get('clk', 0) == 1 or row.get('clk', 0) is True)
        else:
            pos = (edge == 'posedge' or edge == 1 or edge is True)
        if pos and not rst:
            sh = int(row.get('filter_select', 0)) & 3
            i1 = s(row.get('in_1', 0))
            i2 = s(row.get('in_2', 0))
            i3 = s(row.get('in_3', 0))
            o1 = o1 + ((i1 - o1) >> sh)
            o2 = o2 + ((i2 - o2) >> sh)
            o3 = o3 + ((i3 - o3) >> sh)
            if o1 > 32767:
                o1 = 32767
            elif o1 < -32768:
                o1 = -32768
            if o2 > 32767:
                o2 = 32767
            elif o2 < -32768:
                o2 = -32768
            if o3 > 32767:
                o3 = 32767
            elif o3 < -32768:
                o3 = -32768
    return res
