def reference(vectors):
    q = 0
    out = []
    for row in vectors:
        q = row['r_in'] if row['L'] else row['q_in']
        out.append({'Q': q & 1})
    return out
