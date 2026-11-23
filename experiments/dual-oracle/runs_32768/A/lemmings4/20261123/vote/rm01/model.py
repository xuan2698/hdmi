def reference(vectors):
    state = 0
    fall = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            areset = int(row.get('areset', 0))
            bump_left = int(row.get('bump_left', 0))
            bump_right = int(row.get('bump_right', 0))
            ground = int(row.get('ground', 0))
            dig = int(row.get('dig', 0))
        else:
            areset, bump_left, bump_right, ground, dig = [int(x) for x in row]

        if areset:
            state = 0
            fall = 0
        else:
            if state == 0:
                if not ground:
                    state = 2
                    fall = 1
                elif dig:
                    state = 4
                elif bump_left:
                    state = 1
            elif state == 1:
                if not ground:
                    state = 3
                    fall = 1
                elif dig:
                    state = 5
                elif bump_right:
                    state = 0
            elif state == 4:
                if not ground:
                    state = 2
                    fall = 1
            elif state == 5:
                if not ground:
                    state = 3
                    fall = 1
            elif state == 2:
                if ground:
                    if fall > 20:
                        state = 6
                    else:
                        state = 0
                    fall = 0
                else:
                    fall += 1
            elif state == 3:
                if ground:
                    if fall > 20:
                        state = 6
                    else:
                        state = 1
                    fall = 0
                else:
                    fall += 1

        result.append({
            'walk_left': 1 if state == 0 else 0,
            'walk_right': 1 if state == 1 else 0,
            'aaah': 1 if state in (2, 3) else 0,
            'digging': 1 if state in (4, 5) else 0
        })
    return result
