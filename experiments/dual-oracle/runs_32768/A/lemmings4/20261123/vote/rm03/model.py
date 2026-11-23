def reference(vectors):
    state = 0  # 0 WL, 1 WR, 2 FL, 3 FR, 4 DL, 5 DR, 6 DEAD
    fall_count = 0
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
            state = 0
            fall_count = 0
        else:
            if state == 0:  # walk left
                if ground == 0:
                    state = 2
                    fall_count = 1
                elif dig:
                    state = 4
                elif bump_left:
                    state = 1
            elif state == 1:  # walk right
                if ground == 0:
                    state = 3
                    fall_count = 1
                elif dig:
                    state = 5
                elif bump_right:
                    state = 0
            elif state == 2:  # fall left
                if ground:
                    if fall_count > 20:
                        state = 6
                    else:
                        state = 0
                    fall_count = 0
                else:
                    if fall_count < 21:
                        fall_count += 1
            elif state == 3:  # fall right
                if ground:
                    if fall_count > 20:
                        state = 6
                    else:
                        state = 1
                    fall_count = 0
                else:
                    if fall_count < 21:
                        fall_count += 1
            elif state == 4:  # dig left
                if ground == 0:
                    state = 2
                    fall_count = 1
            elif state == 5:  # dig right
                if ground == 0:
                    state = 3
                    fall_count = 1
            elif state == 6:  # dead
                state = 6

        walk_left = 1 if state == 0 else 0
        walk_right = 1 if state == 1 else 0
        aaah = 1 if state in (2, 3) else 0
        digging = 1 if state in (4, 5) else 0

        result.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging
        })

    return result
