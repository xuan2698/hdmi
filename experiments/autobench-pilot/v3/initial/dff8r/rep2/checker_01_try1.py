def reference(vectors):
    q = [0] * 8
    out = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)
        if reset:
            q = [0] * 8
        else:
            q = [(d >> i) & 1 for i in range(8)]
        mid = row.get('mid')
        if mid:
            if mid.get('reset', 0):
                q = [0] * 8
            elif 'd' in mid:
                d2 = mid['d']
                q = [(d2 >> i) & 1 for i in range(8)]
        val = 0
        for i in range(8):
            val |= q[i] << i
        out.append({'q': val})
    return out
