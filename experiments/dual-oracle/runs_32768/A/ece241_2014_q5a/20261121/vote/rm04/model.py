def reference(vectors):
    if isinstance(vectors, dict) and all(isinstance(v, list) for v in vectors.values()):
        keys = list(vectors.keys())
        n = len(vectors[keys[0]]) if keys else 0
        rows = [{k: vectors[k][i] for k in keys} for i in range(n)]
    else:
        rows = vectors

    state = 0  # 0: no 1 yet, 1: seen with output 1, 2: seen with output 0
    result = []

    for row in rows:
        areset = int(row.get("areset", 0))
        x = int(row.get("x", 0))

        if areset:
            state = 0
        elif state == 0:
            state = 1 if x else 0
        elif state == 1:
            state = 2 if x else 1
        else:
            state = 2 if x else 1

        result.append({"z": 1 if state == 1 else 0})

    return result
