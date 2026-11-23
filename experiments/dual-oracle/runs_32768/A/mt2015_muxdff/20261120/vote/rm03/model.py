def reference(vectors):
    if isinstance(vectors, dict):
        keys = list(vectors.keys())
        rows = [{k: vectors[k][i] for k in keys} for i in range(len(vectors[keys[0]]) if keys else 0)]
    else:
        rows = vectors
    out = []
    for row in rows:
        L = row['L']
        q_in = row['q_in']
        r_in = row['r_in']
        out.append({'Q': (r_in if L else q_in) & 1})
    return out
