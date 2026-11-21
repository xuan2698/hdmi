def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        d = row.get('d', 0)
        reset = row.get('reset', 0)
        if reset:
            q = 0
        else:
            q = d & 0xFF
        out.append({'q': q})
        mid = row.get('mid')
        if mid:
            if mid.get('reset', 0):
                q = 0
            elif 'd' in mid:
                q = mid['d'] & 0xFF
    return out
