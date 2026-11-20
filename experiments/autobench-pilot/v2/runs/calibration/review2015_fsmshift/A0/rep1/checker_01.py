def reference(vectors):
    results = []
    count = 0
    for v in vectors:
        reset = v.get('reset', 0)
        if reset:
            count = 4
        if count > 0:
            shift_ena = 1
            count -= 1
        else:
            shift_ena = 0
        results.append({'shift_ena': shift_ena})
    return results
