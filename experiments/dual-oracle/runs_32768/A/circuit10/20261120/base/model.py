def reference(vectors):
    state = 0
    a = 0
    b = 0
    out = []
    for row in vectors:
        if 'a' in row:
            a = row['a']
        if 'b' in row:
            b = row['b']
        new_state = (a & b) | (a & state) | (b & state)
        state = new_state
        q = state ^ a ^ b
        out.append({'q': q, 'state': state})
        mid = row.get('mid', {})
        if 'a' in mid:
            a = mid['a']
        if 'b' in mid:
            b = mid['b']
    return out
