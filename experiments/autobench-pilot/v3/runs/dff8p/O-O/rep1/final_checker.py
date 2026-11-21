def reference(vectors):
    q = 0x34
    out = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)
        if reset:
            q = 0x34
        else:
            q = d & 0xFF
        out.append({'q': q})
        if 'mid' in row:
            m = row['mid']
            if m.get('reset', 0):
                q = 0x34
            elif 'd' in m:
                q = m['d'] & 0xFF
    return out
