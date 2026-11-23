def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)
        if areset:
            state = 0
            z = 0
        else:
            if state == 0:
                state = 1 if x else 0
            else:
                state = 2 if x else 1
            z = 1 if state == 1 else 0
        result.append({'z': z})
    return result
