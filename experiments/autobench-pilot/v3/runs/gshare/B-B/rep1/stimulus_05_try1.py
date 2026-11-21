def stimulus(rng, cycles):
    rows = []
    def r():
        return {
            'areset': 0, 'predict_valid': 0, 'predict_pc': 0,
            'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
            'train_history': 0, 'train_pc': 0
        }
    rows.append({'areset': 1, 'predict_valid': 0, 'predict_pc': 0,
                 'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
                 'train_history': 0, 'train_pc': 0})
    rows.append({'areset': 0, 'predict_valid': 0, 'predict_pc': 0,
                 'train_valid': 0, 'train_taken': 0, 'train_mispredicted': 0,
                 'train_history': 0, 'train_pc': 0})
    for i in range(cycles - 2):
        row = r()
        row['predict_valid'] = rng.getrandbits(1)
        row['predict_pc'] = rng.getrandbits(7)
        row['train_valid'] = rng.getrandbits(1)
        row['train_taken'] = rng.getrandbits(1)
        row['train_mispredicted'] = rng.getrandbits(1)
        row['train_history'] = rng.getrandbits(7)
        row['train_pc'] = rng.getrandbits(7)
        if i % 5 == 0:
            row['train_valid'] = 1
            row['train_mispredicted'] = 1
        if i % 7 == 0:
            row['predict_valid'] = 1
        if i % 11 == 0:
            row['train_valid'] = 1
            row['predict_valid'] = 1
        rows.append(row)
    return rows[:cycles]
