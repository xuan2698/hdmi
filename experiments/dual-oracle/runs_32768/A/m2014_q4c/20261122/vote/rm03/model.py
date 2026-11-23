def reference(vectors):
    q = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            d = row['d']
            r = row['r']
        else:
            d, r = row[0], row[1]
        q = 0 if r else d
        result.append({'q': q})
    return result
