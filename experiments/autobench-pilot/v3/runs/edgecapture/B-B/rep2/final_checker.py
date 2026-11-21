def reference(vectors):
    out = []
    prev = 0
    state = 0
    for row in vectors:
        if row.get('reset', 0):
            state = 0
        else:
            state |= prev & ~row['in']
        state &= 0xFFFFFFFF
        out.append({'out': state})
        prev = row['in'] & 0xFFFFFFFF
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
            elif 'in' in m:
                state |= prev & ~m['in']
                state &= 0xFFFFFFFF
                prev = m['in'] & 0xFFFFFFFF
    return out
