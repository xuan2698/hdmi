def reference(vectors):
    result = []
    for row in vectors:
        L = row['L'] & 1
        q_in = row['q_in'] & 1
        r_in = row['r_in'] & 1
        result.append({'Q': r_in if L else q_in})
    return result
