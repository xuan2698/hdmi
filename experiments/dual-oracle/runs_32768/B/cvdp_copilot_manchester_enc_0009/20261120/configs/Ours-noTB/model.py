def reference(vectors):
    ev = ed = dv = dd = 0
    out = []
    for r in vectors:
        rst = r.get("rst_in", 0)
        if rst:
            ev = ed = dv = dd = 0
        out.append({
            "enc_valid_out": ev & 1,
            "enc_data_out": ed & 0xFFFF,
            "dec_valid_out": dv & 1,
            "dec_data_out": dd & 0xFF
        })
        e = r.get("edge", r.get("clk_in", 0))
        pos = (e == "posedge" or e == 1 or e == "1" or e == True)
        if pos and not rst:
            ev = r.get("enc_valid_in", 0) & 1
            x = r.get("enc_data_in", 0) & 0xFF
            y = 0
            for i in range(8):
                if (x >> i) & 1:
                    y |= 1 << (2 * i)
                else:
                    y |= 2 << (2 * i)
            ed = y & 0xFFFF
            dv = r.get("dec_valid_in", 0) & 1
            z = r.get("dec_data_in", 0) & 0xFFFF
            w = 0
            for i in range(8):
                p = (z >> (2 * i)) & 3
                if p == 1:
                    w |= 1 << i
            dd = w & 0xFF
    return out
