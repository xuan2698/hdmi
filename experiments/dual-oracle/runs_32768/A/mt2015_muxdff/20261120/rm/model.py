def reference(vectors):
    return [{'Q': (v['r_in'] if v['L'] else v['q_in']) & 1} for v in vectors]
