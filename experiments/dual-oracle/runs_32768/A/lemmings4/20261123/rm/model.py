def reference(vectors):
    mode = 0  # 0=walk, 1=fall, 2=dig, 3=splat
    direction = 0  # 0=left, 1=right
    fall_count = 0
    result = []

    for v in vectors:
        areset = v.get('areset', 0)
        bump_left = v.get('bump_left', 0)
        bump_right = v.get('bump_right', 0)
        ground = v.get('ground', 1)
        dig = v.get('dig', 0)

        if areset:
            mode = 0
            direction = 0
            fall_count = 0
        else:
            if mode == 0:
                if ground == 0:
                    mode = 1
                    fall_count = 1
                elif dig:
                    mode = 2
                else:
                    if direction == 0:
                        if bump_left:
                            direction = 1
                    else:
                        if bump_right:
                            direction = 0
            elif mode == 1:
                if ground == 0:
                    fall_count += 1
                else:
                    if fall_count > 20:
                        mode = 3
                    else:
                        mode = 0
                    fall_count = 0
            elif mode == 2:
                if ground == 0:
                    mode = 1
                    fall_count = 1

        walk_left = 1 if mode == 0 and direction == 0 else 0
        walk_right = 1 if mode == 0 and direction == 1 else 0
        aaah = 1 if mode == 1 else 0
        digging = 1 if mode == 2 else 0

        result.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging
        })

    return result
