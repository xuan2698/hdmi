def reference(vectors):
    return [{'Q': (row['r_in'] if row['L'] else row['q_in']) & 1} for row in vectors]
