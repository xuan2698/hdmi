def reference(vectors):
    state = 0  # A
    result = []
    for v in vectors:
        inp = v.get('in', 0)
        rst = v.get('reset', 0)
        if rst:
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
