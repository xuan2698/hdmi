def stimulus(rng, cycles):
    result = []
    q = 0
    for i in range(cycles):
        if i == 0:
            j = 0
            k = 0
        elif i == 1:
            j = 1
            k = 0
        elif i == 2:
            j = 0
            k = 1
        elif i == 3:
            j = 1
            k = 1
        elif i == 4:
            j = 1
            k = 1
        elif i == 5:
            j = 0
            k = 0
        elif i == 6:
            j = 1
            k = 0
        elif i == 7:
            j = 0
            k = 1
        elif i == 8:
            j = 1
            k = 1
        elif i == 9:
            j = 0
            k = 0
        else:
            r = rng.randrange(4)
            j = (r >> 1) & 1
            k = r & 1
        result.append({'j': j, 'k': k})
    return result
