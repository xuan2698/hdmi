def reference(vectors):
    state = 0  # 0=WL, 1=WR, 2=FL, 3=FR, 4=DL, 5=DR, 6=DEAD
    fall_cycles = 0
    result = []
    for row in vectors:
        if isinstance(row, dict):
            areset = int(row.get('areset', 0))
            bump_left = int(row.get('bump_left', 0))
            bump_right = int(row.get('bump_right', 0))
            ground = int(row.get('ground', 0))
            dig = int(row.get('dig', 0))
        else:
            areset = int(row[0])
            bump_left = int(row[1])
            bump_right = int(row[2])
            ground = int(row[3])
            dig = int(row[4])

        if areset:
            state = 0
            fall_cycles = 0
        else:
            if state == 0 or state == 1:  # walking
                if ground == 0:
                    state = 2 if state == 0 else 3
                    fall_cycles = 1
                else:
                    if dig:
                        state = 4 if state == 0 else 5
                    else:
                        if bump_left and bump_right:
                            state = 1 if state == 0 else 0
                        elif bump_left:
                            state = 1
                        elif bump_right:
                            state = 0
            elif state == 2 or state == 3:  # falling
                if ground == 0:
                    fall_cycles += 1
                else:
                    if fall_cycles > 20:
                        state = 6
                    else:
                        state = 0 if state == 2 else 1
                    fall_cycles = 0
            elif state == 4 or state == 5:  # digging
                if ground == 0:
                    state = 2 if state == 4 else 3
                    fall_cycles = 1
            elif state == 6:  # dead
                pass

        walk_left = 1 if state == 0 else 0
        walk_right = 1 if state == 1 else 0
        aaah = 1 if state == 2 or state == 3 else 0
        digging = 1 if state == 4 or state == 5 else 0
        result.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging
        })
    return result
