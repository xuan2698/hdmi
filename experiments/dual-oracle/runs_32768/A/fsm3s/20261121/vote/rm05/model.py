def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        reset = row.get('reset', 0)
        inp = row.get('in', 0)
        if reset:
            state = 0
        else:
            if state == 0:
                state = 1 if inp else 0
            elif state == 1:
                state = 1 if inp else 2
            elif state == 2:
                state = 3 if inp else 0
            else:
                state = 1 if inp else 2
        result.append({'out': 1 if state == 3 else 0})
    return result
