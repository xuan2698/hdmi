def reference(vectors):
    result = []
    for row in vectors:
        if isinstance(row, dict):
            d = int(row['d'])
            r = int(row['r'])
        else:
            d = int(row[0])
            r = int(row[1])
        q = 0 if (r & 1) else (d & 1)
        result.append({'q': q & 1})
    return result
