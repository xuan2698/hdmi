def reference(vectors):
    q = 0
    reset = 0
    out = []
    for row in vectors:
        if 'reset' in row:
            reset = row['reset'] & 1
        if reset:
            nq = 0
        else:
            nq = 0
            carry = 1
            for i in range(4):
                d = (q >> (4 * i)) & 0xF
                if carry:
                    if d == 9:
                        d = 0
                    else:
                        d += 1
                        carry = 0
                nq |= (d & 0xF) << (4 * i)
        q = nq & 0xFFFF
        d0 = q & 0xF
        d1 = (q >> 4) & 0xF
        d2 = (q >> 8) & 0xF
        e0 = 1 if d0 == 9 else 0
        e1 = 1 if (d0 == 9 and d1 == 9) else 0
        e2 = 1 if (d0 == 9 and d1 == 9 and d2 == 9) else 0
        ena = e0 | (e1 << 1) | (e2 << 2)
        out.append({'ena': ena & 0x7, 'q': q & 0xFFFF})
        mid = row.get('mid', {})
        if 'reset' in mid:
            reset = mid['reset'] & 1
    return out
