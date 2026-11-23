def reference(vectors):
    mode = 'walk'  # walk, dig, fall, splat
    direction = 0  # 0 = left, 1 = right
    fall_count = 0

    if isinstance(vectors, dict):
        keys = ['areset', 'bump_left', 'bump_right', 'ground', 'dig']
        n = 0
        for k in keys:
            if k in vectors:
                n = len(vectors[k])
                break
        rows = []
        for i in range(n):
            rows.append({k: vectors.get(k, [0] * n)[i] for k in keys})
        vectors = rows

    result = []

    for row in vectors:
        if isinstance(row, dict):
            areset = row.get('areset', 0)
            bump_left = row.get('bump_left', 0)
            bump_right = row.get('bump_right', 0)
            ground = row.get('ground', 0)
            dig = row.get('dig', 0)
        else:
            areset, bump_left, bump_right, ground, dig = row[0], row[1], row[2], row[3], row[4]

        if areset:
            mode = 'walk'
            direction = 0
            fall_count = 0
        else:
            if mode == 'walk':
                if not ground:
                    mode = 'fall'
                    fall_count = 0
                elif dig:
                    mode = 'dig'
                else:
                    if direction == 0:
                        if bump_left:
                            direction = 1
                    else:
                        if bump_right:
                            direction = 0

            elif mode == 'dig':
                if not ground:
                    mode = 'fall'
                    fall_count = 0

            elif mode == 'fall':
                if ground:
                    if fall_count > 20:
                        mode = 'splat'
                    else:
                        mode = 'walk'
                    fall_count = 0
                else:
                    fall_count += 1

            elif mode == 'splat':
                pass

        walk_left = 1 if mode == 'walk' and direction == 0 else 0
        walk_right = 1 if mode == 'walk' and direction == 1 else 0
        aaah = 1 if mode == 'fall' else 0
        digging = 1 if mode == 'dig' else 0

        result.append({
            'walk_left': walk_left,
            'walk_right': walk_right,
            'aaah': aaah,
            'digging': digging
        })

    return result
