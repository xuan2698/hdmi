def reference(vectors):
    state = 0
    outputs = []
    for row in vectors:
        reset = row["reset"]
        data = row["data"]
        if reset:
            state = 0
            start_shifting = 0
        else:
            if state == 0:
                if data == 1:
                    state = 1
            elif state == 1:
                state = 2 if data == 1 else 0
            elif state == 2:
                state = 3 if data == 0 else 2
            elif state == 3:
                if data == 1:
                    state = 4
                else:
                    state = 0
            start_shifting = 1 if state == 4 else 0
        outputs.append({"start_shifting": start_shifting})
    return outputs
