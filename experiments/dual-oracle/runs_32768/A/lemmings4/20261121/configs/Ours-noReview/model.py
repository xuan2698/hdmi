def reference(vectors):
    mode = 0       # 0=walk, 1=fall, 2=dig, 3=splat
    direction = 0  # 0=left, 1=right
    fall_count = 0
    out = []

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
            mode = 0
            direction = 0
            fall_count = 0
        elif mode == 3:
            pass
        elif mode == 1:
            fall_count += 1
            if ground == 1:
                if fall_count > 20:
                    mode = 3
                else:
                    mode = 0
                fall_count = 0
        elif mode == 0:
            if ground == 0:
                mode = 1
                fall_count = 0
            elif dig == 1:
                mode = 2
            elif direction == 0:
                if bump_left == 1:
                    direction = 1
            else:
                if bump_right == 1:
                    direction = 0
        elif mode == 2:
            if ground == 0:
                mode = 1
                fall_count = 0

        walk_left = 0
        walk_right = 0
        aaah = 0
        digging = 0

        if mode == 1:
            aaah = 1
        elif mode == 2:
            digging = 1
        elif mode == 0:
            if direction == 0:
                walk_left = 1
            else:
                walk_right = 1

        out.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging
        })

    return out
