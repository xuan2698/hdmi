def stimulus(rng, cycles):
    rows = []
    q = 0
    for i in range(cycles):
        if i < 16:
            if i == 0:
                rows.append({'reset': 1})
            elif i == 1:
                rows.append({'reset': 0})
            elif i == 2:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            elif i == 3:
                rows.append({'reset': 0})
            elif i == 4:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            elif i == 5:
                rows.append({'reset': 0})
            elif i == 6:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            elif i == 7:
                rows.append({'reset': 0})
            elif i == 8:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            elif i == 9:
                rows.append({'reset': 0})
            elif i == 10:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            elif i == 11:
                rows.append({'reset': 0})
            elif i == 12:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            elif i == 13:
                rows.append({'reset': 0})
            elif i == 14:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            else:
                rows.append({'reset': 0})
        else:
            r = rng.randrange(4)
            if r == 0:
                rows.append({'reset': 1})
            elif r == 1:
                rows.append({'reset': 0, 'mid': {'reset': 1}})
            else:
                rows.append({'reset': 0})
    return rows
