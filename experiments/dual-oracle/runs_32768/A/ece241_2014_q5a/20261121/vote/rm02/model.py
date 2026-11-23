def reference(vectors):
    state = 'A'
    result = []
    for row in vectors:
        if row['areset']:
            state = 'A'
        else:
            x = row['x']
            if state == 'A':
                state = 'B' if x else 'A'
            elif state == 'B':
                state = 'C' if x else 'B'
            else:  # state == 'C'
                state = 'C' if x else 'B'
        result.append({'z': 1 if state == 'B' else 0})
    return result
