def reference(vectors):
    Q = 0
    result = []
    for v in vectors:
        L = v.get('L', 0)
        q_in = v.get('q_in', 0)
        r_in = v.get('r_in', 0)
        if L == 1:
            Q = r_in
        else:
            Q = q_in
        result.append({'Q': Q})
    return result