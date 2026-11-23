def reference(vectors):
    state = 0
    outputs = []
    for row in vectors:
        areset = row.get('areset', 0)
        x = row.get('x', 0)

        if areset:
            state = 0
            z = 0
        else:
            if state == 0:
                state = 1 if x else 0
            elif state == 1:
                state = 2 if x == 0 else 3
            elif state == 2:
                state = 2 if x == 0 else 3
            else:
                state = 2 if x == 0 else 3

            z = 0 if state == 0 or state == 3 else 1

        outputs.append({'z': z})

    return outputs
