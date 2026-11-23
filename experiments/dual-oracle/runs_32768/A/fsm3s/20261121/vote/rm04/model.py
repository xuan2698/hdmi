def reference(vectors):
    A, B, C, D = 0, 1, 2, 3
    state = A
    result = []

    for row in vectors:
        reset = row['reset']
        inp = row['in']

        if reset:
            state = A
        elif state == A:
            state = B if inp else A
        elif state == B:
            state = B if inp else C
        elif state == C:
            state = D if inp else A
        else:  # state == D
            state = B if inp else C

        result.append({'out': 1 if state == D else 0})

    return result
