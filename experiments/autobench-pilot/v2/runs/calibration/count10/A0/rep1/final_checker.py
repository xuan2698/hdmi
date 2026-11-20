def reference(vectors):
    result = []
    q = 0
    for row in vectors:
        reset = row.get('reset', 0)
        if reset:
            q = 0
        else:
            q = (q + 1) % 10
        result.append({'q': q & 0xF})
    return result
