def reference(vectors):
    out_bits = [None] * 32
    prev_bits = [None] * 32
    result = []
    for row in vectors:
        reset = row['reset']
        inval = row['in'] & 0xFFFFFFFF
        new_out = [None] * 32
        for i in range(32):
            in_i = (inval >> i) & 1
            if reset:
                new_out[i] = 0
            else:
                if in_i == 1:
                    cap = 0
                else:
                    cap = prev_bits[i]
                o = out_bits[i]
                if o == 1 or cap == 1:
                    new_out[i] = 1
                elif o == 0 and cap == 0:
                    new_out[i] = 0
                else:
                    new_out[i] = None
        out_bits = new_out
        new_prev = [None] * 32
        for i in range(32):
            new_prev[i] = (inval >> i) & 1
        prev_bits = new_prev
        unknown = False
        val = 0
        for i in range(32):
            b = out_bits[i]
            if b is None:
                unknown = True
            elif b == 1:
                val |= (1 << i)
        if unknown:
            result.append({'out': None})
        else:
            result.append({'out': val})
    return result
