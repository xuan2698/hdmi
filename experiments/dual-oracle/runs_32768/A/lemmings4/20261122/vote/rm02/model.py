def reference(vectors):
    state = 'L'
    count = 0
    result = []

    for row in vectors:
        if isinstance(row, dict):
            areset = row.get('areset', 0)
            bump_left = row.get('bump_left', 0)
            bump_right = row.get('bump_right', 0)
            ground = row.get('ground', 0)
            dig = row.get('dig', 0)
        else:
            areset, bump_left, bump_right, ground, dig = row[:5]

        if areset:
            state = 'L'
            count = 0

        elif state == 'L':
            if not ground:
                state = 'FL'
                count = 1
            elif dig:
                state = 'DL'
                count = 0
            elif bump_left:
                state = 'R'

        elif state == 'R':
            if not ground:
                state = 'FR'
                count = 1
            elif dig:
                state = 'DR'
                count = 0
            elif bump_right:
                state = 'L'

        elif state == 'DL':
            if not ground:
                state = 'FL'
                count = 1

        elif state == 'DR':
            if not ground:
                state = 'FR'
                count = 1

        elif state == 'FL':
            if ground:
                if count > 20:
                    state = 'S'
                else:
                    state = 'L'
                count = 0
            else:
                count += 1

        elif state == 'FR':
            if ground:
                if count > 20:
                    state = 'S'
                else:
                    state = 'R'
                count = 0
            else:
                count += 1

        elif state == 'S':
            state = 'S'

        result.append({
            'walk_left': 1 if state == 'L' else 0,
            'walk_right': 1 if state == 'R' else 0,
            'aaah': 1 if state in ('FL', 'FR') else 0,
            'digging': 1 if state in ('DL', 'DR') else 0
        })

    return result
