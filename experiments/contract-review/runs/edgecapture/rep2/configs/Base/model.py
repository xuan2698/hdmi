def reference(vectors):
    out = []
    prev = 0
    state = 0
    for row in vectors:
        if row.get('reset', 0):
            state = 0
        else:
            state |= prev & ~row['in']
        out.append({'out': state & 0xFFFFFFFF})
        prev = row['in']
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                state = 0
            elif 'in' in m:
                state |= prev & ~m['in']
                prev = m['in']
    return out
