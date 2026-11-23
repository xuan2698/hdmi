def reference(vectors):
    q = 0
    d = 0
    r = 0
    out = []
    for row in vectors:
        if 'd' in row:
            d = row['d'] & 255
        if 'reset' in row:
            r = row['reset']
        q = 0 if r else (d & 255)
        out.append({'q': q & 255})
        mid = row.get('mid', {})
        if 'd' in mid:
            d = mid['d'] & 255
        if 'reset' in mid:
            r = mid['reset']
    return out
