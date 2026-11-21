def stimulus(rng, cycles):
    rows = []
    rows.append({'L': 1, 'q_in': 0, 'r_in': 0})
    rows.append({'L': 0, 'q_in': 1, 'r_in': 1})
    rows.append({'L': 1, 'q_in': 0, 'r_in': 1})
    rows.append({'L': 0, 'q_in': 1, 'r_in': 0})
    rows.append({'L': 1, 'q_in': 1, 'r_in': 0})
    rows.append({'L': 0, 'q_in': 0, 'r_in': 1})
    rows.append({'L': 1, 'q_in': 1, 'r_in': 1})
    rows.append({'L': 0, 'q_in': 0, 'r_in': 0})
    while len(rows) < cycles:
        L = rng.getrandbits(1)
        q_in = rng.getrandbits(1)
        r_in = rng.getrandbits(1)
        row = {'L': L, 'q_in': q_in, 'r_in': r_in}
        if rng.random() < 0.3:
            row['mid'] = {'L': rng.getrandbits(1), 'q_in': rng.getrandbits(1), 'r_in': rng.getrandbits(1)}
        rows.append(row)
    return rows[:cycles]
