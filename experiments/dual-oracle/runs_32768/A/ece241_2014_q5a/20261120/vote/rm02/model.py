def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        if row['areset']:
            state = 0
        else:
            x = row['x']
            if state == 0:
                state = 1 if x else 0
            else:
                state = 2 if x else 1
        result.append({'z': 1 if state == 1 else 0})
    return result
