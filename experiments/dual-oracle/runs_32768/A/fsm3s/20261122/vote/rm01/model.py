def reference(vectors):
    state = 0
    outputs = []
    for v in vectors:
        if v['reset']:
            state = 0
        else:
            i = v['in']
            if state == 0:
                state = 1 if i else 0
            elif state == 1:
                state = 1 if i else 2
            elif state == 2:
                state = 3 if i else 0
            else:
                state = 1 if i else 2
        outputs.append({'out': 1 if state == 3 else 0})
    return outputs
