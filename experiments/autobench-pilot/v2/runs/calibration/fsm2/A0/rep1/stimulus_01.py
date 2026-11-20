def stimulus(rng, cycles):
    result = []
    state = 0  # 0 = OFF, 1 = ON
    i = 0
    while i < cycles:
        d = {}
        # Occasionally assert asynchronous reset
        if rng.random() < 0.1:
            d['areset'] = 1
            d['j'] = rng.getrandbits(1)
            d['k'] = rng.getrandbits(1)
            state = 0
        else:
            d['areset'] = 0
            # Bias inputs toward transitions based on current state
            if state == 0:
                # j=1 -> ON, j=0 -> OFF
                if rng.random() < 0.5:
                    d['j'] = 1
                    state = 1
                else:
                    d['j'] = 0
                d['k'] = rng.getrandbits(1)
            else:
                # k=1 -> OFF, k=0 -> ON
                if rng.random() < 0.5:
                    d['k'] = 1
                    state = 0
                else:
                    d['k'] = 0
                d['j'] = rng.getrandbits(1)
        result.append(d)
        i += 1
    return result
