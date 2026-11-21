def stimulus(rng, cycles):
    rows = []
    hist = 0
    pcs = [rng.randrange(128) for _ in range(8)]
    for i in range(cycles):
        r = {}
        r['areset'] = 1 if i == 0 else 0
        r['predict_valid'] = rng.getrandbits(1)
        r['predict_pc'] = rng.choice(pcs) if rng.random() < 0.7 else rng.randrange(128)
        r['train_valid'] = rng.getrandbits(1)
        r['train_taken'] = rng.getrandbits(1)
        r['train_mispredicted'] = rng.getrandbits(1) if r['train_valid'] else 0
        r['train_history'] = rng.randrange(128)
        r['train_pc'] = rng.choice(pcs) if rng.random() < 0.7 else rng.randrange(128)
        if i < 16:
            if i == 1:
                r['predict_valid'] = 1
                r['train_valid'] = 0
            elif i == 2:
                r['predict_valid'] = 0
                r['train_valid'] = 1
                r['train_mispredicted'] = 1
            elif i == 3:
                r['predict_valid'] = 1
                r['train_valid'] = 1
                r['train_mispredicted'] = 1
            elif i == 4:
                r['predict_valid'] = 1
                r['train_valid'] = 1
                r['train_mispredicted'] = 0
            elif i == 5:
                r['predict_valid'] = 0
                r['train_valid'] = 0
            elif i == 6:
                r['predict_valid'] = 1
                r['train_valid'] = 0
                r['mid'] = {'predict_valid': 0, 'train_valid': 1, 'train_mispredicted': 1}
            elif i == 7:
                r['predict_valid'] = 1
                r['train_valid'] = 1
                r['mid'] = {'train_mispredicted': 0}
            elif i == 8:
                r['predict_valid'] = 1
                r['train_valid'] = 0
                r['mid'] = {'predict_pc': (r['predict_pc'] + 1) % 128}
            elif i == 9:
                r['predict_valid'] = 0
                r['train_valid'] = 1
                r['mid'] = {'train_taken': 1 - r['train_taken']}
            elif i == 10:
                r['predict_valid'] = 1
                r['train_valid'] = 1
                r['mid'] = {'predict_valid': 0}
            elif i == 11:
                r['predict_valid'] = 1
                r['train_valid'] = 0
                r['mid'] = {'train_valid': 1, 'train_mispredicted': 1, 'train_history': rng.randrange(128)}
            elif i == 12:
                r['predict_valid'] = 0
                r['train_valid'] = 0
                r['mid'] = {'predict_valid': 1}
            elif i == 13:
                r['predict_valid'] = 1
                r['train_valid'] = 1
                r['mid'] = {'areset': 1}
            elif i == 14:
                r['areset'] = 0
                r['predict_valid'] = 1
                r['train_valid'] = 0
            elif i == 15:
                r['predict_valid'] = 1
                r['train_valid'] = 1
                r['train_mispredicted'] = 1
        rows.append(r)
    return rows
