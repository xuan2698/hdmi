def stimulus(rng, cycles):
    samples = []
    history = 0
    for i in range(cycles):
        areset = 0
        predict_valid = 0
        predict_pc = 0
        train_valid = 0
        train_taken = 0
        train_mispredicted = 0
        train_history = 0
        train_pc = 0

        if i == 0:
            areset = 1
        elif i == 1:
            areset = 0
        else:
            r = rng.randrange(100)
            if r < 5:
                areset = 1
            else:
                areset = 0
                if rng.randrange(2) == 0:
                    predict_valid = 1
                    predict_pc = rng.getrandbits(7)
                if rng.randrange(2) == 0:
                    train_valid = 1
                    train_taken = rng.getrandbits(1)
                    train_mispredicted = rng.getrandbits(1)
                    train_history = rng.getrandbits(7)
                    train_pc = rng.getrandbits(7)
                if rng.randrange(10) == 0:
                    predict_valid = 1
                    predict_pc = rng.getrandbits(7)
                    train_valid = 1
                    train_taken = rng.getrandbits(1)
                    train_mispredicted = rng.getrandbits(1)
                    train_history = rng.getrandbits(7)
                    train_pc = rng.getrandbits(7)

        samples.append({
            'areset': areset,
            'predict_valid': predict_valid,
            'predict_pc': predict_pc,
            'train_valid': train_valid,
            'train_taken': train_taken,
            'train_mispredicted': train_mispredicted,
            'train_history': train_history,
            'train_pc': train_pc,
        })
    return samples
