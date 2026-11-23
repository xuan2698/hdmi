def reference(vectors):
    N = 8
    enc_data_out = 0
    enc_valid_out = 0
    dec_data_out = 0
    dec_valid_out = 0
    result = []

    def encode(v):
        r = 0
        for i in range(N):
            b = (v >> i) & 1
            p = 1 if b else 2
            r |= p << (2 * i)
        return r & 0xFFFF

    def decode(v):
        r = 0
        for i in range(N):
            p = (v >> (2 * i)) & 3
            if p == 1:
                r |= 1 << i
        return r & 0xFF

    for row in vectors:
        rst = int(row.get('rst_in', 0))
        if rst:
            enc_data_out = 0
            enc_valid_out = 0
            dec_data_out = 0
            dec_valid_out = 0

        result.append({
            'enc_valid_out': enc_valid_out,
            'enc_data_out': enc_data_out,
            'dec_valid_out': dec_valid_out,
            'dec_data_out': dec_data_out
        })

        e = row.get('edge', row.get('clk_edge', ''))
        pos = False
        if e is True or e == 1:
            pos = True
        elif isinstance(e, str) and 'pos' in e.lower():
            pos = True

        if pos and rst == 0:
            if int(row.get('enc_valid_in', 0)):
                enc_data_out = encode(int(row.get('enc_data_in', 0)))
                enc_valid_out = 1
            else:
                enc_valid_out = 0

            if int(row.get('dec_valid_in', 0)):
                dec_data_out = decode(int(row.get('dec_data_in', 0)))
                dec_valid_out = 1
            else:
                dec_valid_out = 0

    return result
