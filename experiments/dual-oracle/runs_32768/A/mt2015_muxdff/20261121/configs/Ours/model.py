def reference(vectors):
    result = []
    for v in vectors:
        L = int(v['L']) & 1
        q_in = int(v['q_in']) & 1
        r_in = int(v['r_in']) & 1
        Q = r_in if L else q_in
        result.append({'Q': Q})
    return result
