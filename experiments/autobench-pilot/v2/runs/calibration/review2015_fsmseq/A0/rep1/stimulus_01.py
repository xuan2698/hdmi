def stimulus(rng, cycles):
    result = []
    found = False
    state = 0
    for i in range(cycles):
        reset = 0
        data = 0
        if i == 0:
            reset = 1
            data = rng.getrandbits(1)
        elif i == 1:
            reset = 0
            data = 0
        else:
            r = rng.random()
            if r < 0.05:
                reset = 1
                data = rng.getrandbits(1)
            elif r < 0.15:
                reset = 0
                data = 1
            elif r < 0.25:
                reset = 0
                data = 0
            else:
                if not found:
                    target = [1, 1, 0, 1]
                    if state < 4:
                        data = target[state]
                    else:
                        data = rng.getrandbits(1)
                else:
                    data = rng.getrandbits(1)
        if reset:
            state = 0
            found = False
        else:
            if not found:
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 1 if data == 1 else 0
                    if data == 1:
                        state = 2
                    else:
                        state = 0
                elif state == 2:
                    if data == 0:
                        state = 3
                    else:
                        state = 2
                elif state == 3:
                    if data == 1:
                        state = 4
                        found = True
                    else:
                        state = 0
        result.append({'reset': reset, 'data': data})
    return result
