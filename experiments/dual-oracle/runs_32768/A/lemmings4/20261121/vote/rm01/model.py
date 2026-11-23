def reference(vectors):
    WL, WR, DL, DR, FL, FR, SPLAT = range(7)
    state = WL
    fall_cnt = 0
    result = []

    for row in vectors:
        areset = row['areset']
        bump_left = row['bump_left']
        bump_right = row['bump_right']
        ground = row['ground']
        dig = row['dig']

        if areset:
            state = WL
            fall_cnt = 0
        elif state != SPLAT:
            if state in (FL, FR):
                direction_left = (state == FL)
                if ground:
                    if fall_cnt >= 20:
                        state = SPLAT
                        fall_cnt = 0
                    else:
                        state = WL if direction_left else WR
                        fall_cnt = 0
                else:
                    if fall_cnt < 20:
                        fall_cnt += 1
                    state = FL if direction_left else FR
            else:
                if not ground:
                    if state in (WL, DL):
                        state = FL
                    else:
                        state = FR
                    fall_cnt = 0
                elif state in (WL, WR):
                    if dig:
                        state = DL if state == WL else DR
                    else:
                        if state == WL:
                            state = WR if bump_left else WL
                        else:
                            state = WL if bump_right else WR
                    fall_cnt = 0
                elif state in (DL, DR):
                    state = DL if state == DL else DR
                    fall_cnt = 0

        result.append({
            'walk_left': 1 if state == WL else 0,
            'walk_right': 1 if state == WR else 0,
            'aaah': 1 if state in (FL, FR) else 0,
            'digging': 1 if state in (DL, DR) else 0,
        })

    return result
