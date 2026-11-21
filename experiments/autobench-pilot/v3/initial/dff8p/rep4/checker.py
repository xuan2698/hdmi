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
        mid = row.get('mid')
        if mid:
            if mid.get('reset', 0):
                q = 0x34
            elif 'd' in mid:
                q = mid['d'] & 0xFF
    return out
