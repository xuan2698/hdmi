def stimulus(rng, cycles):
    result = []
    for i in range(cycles):
        load = 1 if rng.random() < 0.15 else 0
        ena = 1 if rng.random() < 0.85 else 0
        amount = rng.randrange(4)
        data = rng.getrandbits(64)
        result.append({'load': load, 'ena': ena, 'amount': amount, 'data': data})
    return result
