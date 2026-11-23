def reference(vectors):
    q = 4
    prev_a = 1
    result = []
    for v in vectors:
        a = v['a']
        if a == 1:
            q = 4
        else:
            if prev_a == 1:
                q = 4
            else:
                q = (q + 1) % 7
        prev_a = a
        result.append({'q': q})
    return result
