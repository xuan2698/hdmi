def reference(vectors):
    if isinstance(vectors, dict):
        keys = ['areset', 'bump_left', 'bump_right', 'ground', 'dig']
        n = 0
        for k in keys:
            if k in vectors and isinstance(vectors[k], (list, tuple)):
                n = len(vectors[k])
                break
        rows = []
        for i in range(n):
            row = {}
            for k in keys:
                v = vectors.get(k, 0)
                row[k] = v[i] if isinstance(v, (list, tuple)) else v
            rows.append(row)
        vectors = rows

    state = 'WL'
    fall_count = 0
    result = []

    for row in vectors:
        if isinstance(row, dict):
            areset = int(row.get('areset', 0)) & 1
            bump_left = int(row.get('bump_left', 0)) & 1
            bump_right = int(row.get('bump_right', 0)) & 1
            ground = int(row.get('ground', 0)) & 1
            dig = int(row.get('dig', 0)) & 1
        else:
            try:
                areset = int(row[0]) & 1
                bump_left = int(row[1]) & 1
                bump_right = int(row[2]) & 1
                ground = int(row[3]) & 1
                dig = int(row[4]) & 1
            except Exception:
                areset = bump_left = bump_right = ground = dig = 0

        if areset:
            state = 'WL'
            fall_count = 0
        else:
            if state in ('WL', 'WR'):
                if ground == 0:
                    state = 'FL' if state == 'WL' else 'FR'
                    fall_count = 0
                elif dig:
                    state = 'DL' if state == 'WL' else 'DR'
                    fall_count = 0
                else:
                    if bump_left and bump_right:
                        state = 'WR' if state == 'WL' else 'WL'
                    elif bump_left:
                        state = 'WR'
                    elif bump_right:
                        state = 'WL'
            elif state in ('FL', 'FR'):
                if ground == 0:
                    fall_count += 1
                else:
                    if fall_count >= 20:
                        state = 'DEAD'
                        fall_count = 0
                    else:
                        state = 'WL' if state == 'FL' else 'WR'
                        fall_count = 0
            elif state in ('DL', 'DR'):
                if ground == 0:
                    state = 'FL' if state == 'DL' else 'FR'
                    fall_count = 0
            elif state == 'DEAD':
                pass

        out = {'walk_left': 0, 'walk_right': 0, 'aaah': 0, 'digging': 0}
        if state == 'WL':
            out['walk_left'] = 1
        elif state == 'WR':
            out['walk_right'] = 1
        elif state in ('FL', 'FR'):
            out['aaah'] = 1
        elif state in ('DL', 'DR'):
            out['digging'] = 1

        result.append(out)

    return result
