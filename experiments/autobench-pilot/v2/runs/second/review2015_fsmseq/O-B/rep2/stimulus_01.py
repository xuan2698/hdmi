def stimulus(rng, cycles):
    out = []
    state = 0
    found = False
    for i in range(cycles):
        reset = 0
        if i == 0:
            reset = 1
        elif rng.random() < 0.05:
            reset = 1
        if reset:
            data = rng.getrandbits(1)
            state = 0
            found = False
        else:
            if not found:
                if state == 0:
                    data = 1 if rng.random() < 0.7 else 0
                elif state == 1:
                    data = 1 if rng.random() < 0.7 else 0
                elif state == 2:
                    data = 0 if rng.random() < 0.7 else 1
                elif state == 3:
                    data = 1 if rng.random() < 0.7 else 0
                else:
                    data = rng.getrandbits(1)
                if state == 0:
                    state = 1 if data == 1 else 0
                elif state == 1:
                    state = 2 if data == 1 else 0
                elif state == 2:
                    state = 3 if data == 0 else 2
                elif state == 3:
                    if data == 1:
                        found = True
                        state = 4
                    else:
                        state = 0
            else:
                data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
