def reference(vectors):
    q = 0
    result = []
    for row in vectors:
        a = row['a']
        if a:
            q = 4
        else:
            q = (q + 1) % 7
        result.append({'q': q})
    return result
