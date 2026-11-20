def stimulus(rng, cycles):
    out = []
    state = 0
    found = False
    for i in range(cycles):
        reset = 0
        data = 0
        if i == 0:
            reset = 1
        elif rng.random() < 0.08:
            reset = 1
        else:
            if not found:
                if state == 0:
                    data = rng.choice([1, 1, 0])
                elif state == 1:
                    data = rng.choice([1, 0])
                elif state == 2:
                    data = rng.choice([0, 1])
                elif state == 3:
                    data = rng.choice([1, 0])
            else:
                data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
        if reset:
            state = 0
            found = False
        else:
            if not found:
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 0
                elif state == 2:
                    state = 3 if data == 0 else 2
                elif state == 3:
                    if data == 1:
                        found = True
                        state = 0
                    else:
                        state = 0
    return out
