def reference(vectors):
    result = []
    state = 1
    for row in vectors:
        reset = row.get('reset', 0)
        if reset:
            state = 1
        else:
            state = state + 1
            if state > 10:
                state = 1
        result.append({'q': state & 0xF})
    return result
