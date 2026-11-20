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
                else:
                    data = 1 if rng.random() < 0.7 else 0
                if state == 0 and data == 1:
                    state = 1
                elif state == 1 and data == 1:
                    state = 2
                elif state == 2 and data == 0:
                    state = 3
                elif state == 3 and data == 1:
                    state = 4
                    found = True
                elif state == 1 and data == 0:
                    state = 0
                elif state == 2 and data == 1:
                    state = 2
                elif state == 3 and data == 0:
                    state = 0
            else:
                data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
