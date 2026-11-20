def stimulus(rng, cycles):
    rows = []
    cooldown = 0
    for i in range(cycles):
        if i == 0:
            reset = 1
            cooldown = 3
        elif cooldown > 0:
            reset = 0
            cooldown -= 1
        else:
            if rng.random() < 0.12:
                reset = 1
                cooldown = 3
            else:
                reset = 0
        rows.append({'reset': reset, 'in': rng.getrandbits(32)})
    return rows
