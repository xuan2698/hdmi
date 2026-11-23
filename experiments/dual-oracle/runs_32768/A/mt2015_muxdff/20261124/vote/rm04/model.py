def reference(vectors):
    Q = 0
    result = []
    for row in vectors:
        L = row['L'] & 1
        q_in = row['q_in'] & 1
        r_in = row['r_in'] & 1
        Q = r_in if L else q_in
        result.append({'Q': Q & 1})
    return result
