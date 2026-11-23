def reference(vectors):
    state = 0
    outputs = []
    for row in vectors:
        rst = int(row.get('reset', 0))
        inp = int(row.get('in', 0))

        if rst:
            state = 0
        elif state == 0:
            state = 1 if inp else 0
        elif state == 1:
            state = 2 if inp == 0 else 1
        elif state == 2:
            state = 3 if inp else 0
        else:
            state = 1 if inp else 2

        outputs.append({'out': 1 if state == 3 else 0})

    return outputs
