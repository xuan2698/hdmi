def stimulus(rng, cycles):
    rows = []
    rows.append({'r_in': 0, 'q_in': 0, 'L': 0})
    rows.append({'r_in': 1, 'q_in': 0, 'L': 1})
    rows.append({'r_in': 1, 'q_in': 1, 'L': 0})
    rows.append({'r_in': 0, 'q_in': 1, 'L': 1})
    rows.append({'r_in': 1, 'q_in': 0, 'L': 0, 'mid': {'L': 1}})
    rows.append({'r_in': 0, 'q_in': 1, 'L': 1, 'mid': {'L': 0}})
    rows.append({'r_in': 1, 'q_in': 1, 'L': 0, 'mid': {'r_in': 0}})
    rows.append({'r_in': 0, 'q_in': 0, 'L': 1, 'mid': {'q_in': 1}})
    while len(rows) < cycles:
        r = rng.getrandbits(1)
        q = rng.getrandbits(1)
        L = rng.getrandbits(1)
        row = {'r_in': r, 'q_in': q, 'L': L}
        if rng.random() < 0.3:
            mid = {}
            if rng.random() < 0.5:
                mid['r_in'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                mid['q_in'] = rng.getrandbits(1)
            if rng.random() < 0.5:
                mid['L'] = rng.getrandbits(1)
            if mid:
                row['mid'] = mid
        rows.append(row)
    return rows[:cycles]
