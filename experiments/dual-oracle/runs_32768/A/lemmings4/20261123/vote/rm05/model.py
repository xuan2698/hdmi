def reference(vectors):
    def getv(row, key, idx):
        if isinstance(row, dict):
            return int(row.get(key, 0))
        return int(row[idx])

    if isinstance(vectors, dict):
        keys = ['areset', 'bump_left', 'bump_right', 'ground', 'dig']
        n = 0
        for v in vectors.values():
            if isinstance(v, (list, tuple)):
                if len(v) > n:
                    n = len(v)
            else:
                if n < 1:
                    n = 1
        rows = []
        for i in range(n):
            d = {}
            for k in keys:
                arr = vectors.get(k, [])
                if isinstance(arr, (list, tuple)):
                    d[k] = int(arr[i]) if i < len(arr) else 0
                else:
                    d[k] = int(arr) if i == 0 else 0
            rows.append(d)
        vectors = rows

    state = 'L'
    count = 0
    out = []

    for row in vectors:
        areset = getv(row, 'areset', 0)
        bump_left = getv(row, 'bump_left', 1)
        bump_right = getv(row, 'bump_right', 2)
        ground = getv(row, 'ground', 3)
        dig = getv(row, 'dig', 4)

        if areset:
            state = 'L'
            count = 0
        else:
            if state == 'L' or state == 'R':
                if ground == 0:
                    state = 'F' + state
                    count = 1
                elif dig:
                    state = 'D' + state
                    count = 0
                else:
                    if state == 'L':
                        if bump_left:
                            state = 'R'
                    else:
                        if bump_right:
                            state = 'L'
            elif state == 'FL' or state == 'FR':
                if ground == 1:
                    if count > 20:
                        state = 'DEAD'
                    else:
                        if state == 'FL':
                            state = 'L'
                        else:
                            state = 'R'
                    count = 0
                else:
                    count += 1
            elif state == 'DL' or state == 'DR':
                if ground == 0:
                    if state == 'DL':
                        state = 'FL'
                    else:
                        state = 'FR'
                    count = 1
            elif state == 'DEAD':
                pass

        wl = 1 if state == 'L' else 0
        wr = 1 if state == 'R' else 0
        aaah = 1 if (state == 'FL' or state == 'FR') else 0
        digging = 1 if (state == 'DL' or state == 'DR') else 0

        out.append({
            'walk_left': wl,
            'walk_right': wr,
            'aaah': aaah,
            'digging': digging
        })

    return out
