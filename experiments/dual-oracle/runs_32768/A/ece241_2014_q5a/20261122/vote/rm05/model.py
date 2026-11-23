def reference(vectors):
    A, B, C = 0, 1, 2
    state = A
    out = []
    for row in vectors:
        areset = int(row.get('areset', 0))
        x = int(row.get('x', 0))
        if areset:
            state = A
        else:
            if state == A:
                state = B if x else A
            elif state == B:
                state = C if x else B
            else:
                state = C if x else B
        out.append({'z': 1 if state == B else 0})
    return out
