def reference(vectors):
    state = 0
    out = []
    for row in vectors:
        a = row.get('a', 0)
        b = row.get('b', 0)
        state = (a & b) | (a & state) | (b & state)
        q = a ^ b ^ state
        out.append({'q': q, 'state': state})
    return out
