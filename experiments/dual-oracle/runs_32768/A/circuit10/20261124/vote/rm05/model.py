def reference(vectors):
    state = 0
    result = []
    for v in vectors:
        a = v['a']
        b = v['b']
        nxt = (a | b) if state else (a & b)
        state = nxt
        q = state ^ a ^ b
        result.append({'q': q, 'state': state})
    return result
