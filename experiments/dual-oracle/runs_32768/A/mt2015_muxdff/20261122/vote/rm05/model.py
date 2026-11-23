def reference(vectors):
    outputs = []
    for v in vectors:
        L = int(v.get('L', 0)) & 1
        q_in = int(v.get('q_in', 0)) & 1
        r_in = int(v.get('r_in', 0)) & 1
        Q = r_in if L else q_in
        outputs.append({'Q': Q})
    return outputs
