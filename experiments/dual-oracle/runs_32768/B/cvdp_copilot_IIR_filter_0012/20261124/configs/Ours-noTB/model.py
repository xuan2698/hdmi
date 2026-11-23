def reference(vectors):
    def s(v):
        v = int(v) & 0xFFFF
        return v - 0x10000 if v & 0x8000 else v
    out1 = out2 = out3 = 0
    res = []
    for row in vectors:
        if row.get('reset', 0):
            out1 = out2 = out3 = 0
        res.append({
            'out_1': out1 & 0xFFFF,
            'out_2': out2 & 0xFFFF,
            'out_3': out3 & 0xFFFF
        })
        clk = row.get('clk', 0)
        if (clk == 1 or clk is True) and not row.get('reset', 0):
            sh = row.get('filter_select', 0)
            in1 = s(row.get('in_1', 0))
            in2 = s(row.get('in_2', 0))
            in3 = s(row.get('in_3', 0))
            out1 = out1 + ((in1 - out1) >> sh)
            out2 = out2 + ((in2 - out2) >> sh)
            out3 = out3 + ((in3 - out3) >> sh)
            if out1 > 32767: out1 = 32767
            elif out1 < -32768: out1 = -32768
            if out2 > 32767: out2 = 32767
            elif out2 < -32768: out2 = -32768
            if out3 > 32767: out3 = 32767
            elif out3 < -32768: out3 = -32768
    return res
