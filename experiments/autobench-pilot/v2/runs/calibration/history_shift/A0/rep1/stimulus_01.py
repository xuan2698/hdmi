def stimulus(rng, cycles):
    result = []
    history = 0
    for i in range(cycles):
        areset = 0
        predict_valid = 0
        predict_taken = 0
        train_mispredicted = 0
        train_taken = 0
        train_history = 0

        if i == 0:
            areset = 1
        elif i == 1:
            areset = 0
            predict_valid = 1
            predict_taken = rng.getrandbits(1)
        elif i == 2:
            predict_valid = 1
            predict_taken = rng.getrandbits(1)
        elif i == 3:
            train_mispredicted = 1
            train_taken = rng.getrandbits(1)
            train_history = rng.getrandbits(32)
        elif i == 4:
            predict_valid = 1
            predict_taken = rng.getrandbits(1)
            train_mispredicted = 1
            train_taken = rng.getrandbits(1)
            train_history = rng.getrandbits(32)
        elif i == 5:
            areset = 1
        elif i == 6:
            predict_valid = 1
            predict_taken = 0
        elif i == 7:
            predict_valid = 1
            predict_taken = 1
        elif i == 8:
            train_mispredicted = 1
            train_taken = 0
            train_history = 0
        elif i == 9:
            train_mispredicted = 1
            train_taken = 1
            train_history = 0xFFFFFFFF
        else:
            r = rng.randrange(8)
            if r == 0:
                areset = 1
            elif r == 1:
                predict_valid = 1
                predict_taken = rng.getrandbits(1)
            elif r == 2:
                train_mispredicted = 1
                train_taken = rng.getrandbits(1)
                train_history = rng.getrandbits(32)
            elif r == 3:
                predict_valid = 1
                predict_taken = rng.getrandbits(1)
                train_mispredicted = 1
                train_taken = rng.getrandbits(1)
                train_history = rng.getrandbits(32)
            elif r == 4:
                predict_valid = 1
                predict_taken = 1
            elif r == 5:
                predict_valid = 1
                predict_taken = 0
            elif r == 6:
                train_mispredicted = 1
                train_taken = 1
                train_history = rng.getrandbits(32)
            else:
                train_mispredicted = 1
                train_taken = 0
                train_history = rng.getrandbits(32)

        result.append({
            'areset': areset,
            'predict_valid': predict_valid,
            'predict_taken': predict_taken,
            'train_mispredicted': train_mispredicted,
            'train_taken': train_taken,
            'train_history': train_history,
        })
    return result
