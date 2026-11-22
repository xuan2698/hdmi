def reference(vectors):
    q = 52
    result = []
    for v in vectors:
        if v['reset']:
            q = 52
        else:
            q = v['d'] & 255
        result.append({'q': q})
    return result