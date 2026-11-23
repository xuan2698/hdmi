def reference(vectors):
    state = 0
    outputs = []
    for row in vectors:
        if isinstance(row, dict):
            inp = row.get('in', 0)
            reset = row.get('reset', 0)
        elif isinstance(row, (list, tuple)):
            inp = row[0] if len(row) > 0 else 0
            reset = row[1] if len(row) > 1 else 0
        else:
            inp = row
            reset = 0
        inp = 1 if inp else 0
        reset = 1 if reset else 0

        if reset:
            state = 0
        elif state == 0:
            state = 1 if inp else 0
        elif state == 1:
            state = 1 if inp else 2
        elif state == 2:
            state = 3 if inp else 0
        else:
            state = 1 if inp else 2

        outputs.append({'out': 1 if state == 3 else 0})
    return outputs
