def reference(vectors):
    mode = 0        # 0=walk, 1=fall, 2=dig, 3=dead
    direction = 0   # 0=left, 1=right
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
            areset = row[0]
            bump_left = row[1]
            bump_right = row[2]
            ground = row[3]
            dig = row[4]

        if areset:
            mode = 0
            direction = 0
            fall_count = 0
        else:
            if mode == 3:
                pass
            elif mode == 0:
                if ground == 0:
                    mode = 1
                    fall_count = 1
                elif dig == 1:
                    mode = 2
                else:
                    if direction == 0:
                        if bump_left:
                            direction = 1
                    else:
                        if bump_right:
                            direction = 0
            elif mode == 1:
                if ground == 1:
                    if fall_count > 20:
                        mode = 3
                    else:
                        mode = 0
                    fall_count = 0
                else:
                    fall_count += 1
            elif mode == 2:
                if ground == 0:
                    mode = 1
                    fall_count = 1

        result.append({
            'walk_left': 1 if mode == 0 and direction == 0 else 0,
            'walk_right': 1 if mode == 0 and direction == 1 else 0,
            'aaah': 1 if mode == 1 else 0,
            'digging': 1 if mode == 2 else 0
        })

    return result
