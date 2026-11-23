def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        inp = row['in']
        reset = row['reset']
        if reset:
            state = 0
        elif state == 0:
            state = 1 if inp else 0
        elif state == 1:
            state = 2 if inp == 0 else 1
        elif state == 2:
            state = 0 if inp == 0 else 3
        else:
            state = 2 if inp == 0 else 1
        result.append({'out': 1 if state == 3 else 0})
    return result
