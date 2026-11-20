def reference(vectors):
    q = 0
    out = []
    for v in vectors:
        if v.get('load'):
            q = v['data'] & ((1 << 512) - 1)
        else:
            nq = 0
            for i in range(512):
                left = (q >> (i + 1)) & 1 if i + 1 < 512 else 0
                center = (q >> i) & 1
                right = (q >> (i - 1)) & 1 if i - 1 >= 0 else 0
                idx = (left << 2) | (center << 1) | right
                nxt = (0b01111110 >> idx) & 1
                nq |= nxt << i
            q = nq
        out.append({'q': q})
    return out
