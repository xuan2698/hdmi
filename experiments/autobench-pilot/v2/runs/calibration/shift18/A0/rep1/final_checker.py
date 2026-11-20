def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        load = v.get('load', 0)
        ena = v.get('ena', 0)
        amount = v.get('amount', 0)
        data = v.get('data', 0)
        if load:
            q = data & ((1 << 64) - 1)
        elif ena:
            if amount == 0:
                q = (q << 1) & ((1 << 64) - 1)
            elif amount == 1:
                q = (q << 8) & ((1 << 64) - 1)
            elif amount == 2:
                # arithmetic right shift by 1
                sign = q >> 63
                q = (q >> 1) | (sign << 63)
                q &= (1 << 64) - 1
            else:  # amount == 3
                sign = q >> 63
                q = (q >> 8) | (sign * 0xFF << 56)
                q &= (1 << 64) - 1
        out.append({'q': q})
    return out
