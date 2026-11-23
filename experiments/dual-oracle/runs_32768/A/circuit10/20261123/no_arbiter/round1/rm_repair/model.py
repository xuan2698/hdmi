def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        a = row['a']
        b = row['b']
        q = a ^ b ^ state
        result.append({'q': q, 'state': state})
        state = (a & b) | (a & state) | (b & state)
    return result
