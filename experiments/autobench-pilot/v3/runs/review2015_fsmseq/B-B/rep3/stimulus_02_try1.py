def stimulus(rng, cycles):
    rows = []
    seq = [1, 1, 0, 1]
    for i in range(cycles):
        if i < 16:
            if i < 4:
                data = seq[i]
            elif i < 8:
                data = rng.getrandbits(1)
            elif i < 12:
                data = [1, 1, 0, 1][i % 4]
            else:
                data = rng.choice([0, 1])
            reset = 1 if i == 0 else 0
            row = {'reset': reset, 'data': data}
            if i % 5 == 2:
                row['mid'] = {'data': rng.getrandbits(1)}
            rows.append(row)
        else:
            data = rng.getrandbits(1)
            reset = 1 if rng.randrange(20) == 0 else 0
            row = {'reset': reset, 'data': data}
            if rng.randrange(3) == 0:
                row['mid'] = {'data': rng.getrandbits(1)}
            rows.append(row)
    return rows
