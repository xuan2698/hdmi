def reference(vectors):
    out = []
    state = 0  # OFF
    for v in vectors:
        if v.get('areset'):
            state = 0
        else:
            if state == 0:
                if v.get('j'):
                    state = 1
            else:
                if v.get('k'):
                    state = 0
        out.append({'out': state})
    return out
