def stimulus(rng, cycles):
    rows = []
    rows.append({'r_in': 0, 'L': 1, 'q_in': 0})
    rows.append({'r_in': 7, 'L': 1, 'q_in': 1})
    rows.append({'r_in': 5, 'L': 0, 'q_in': 0})
    rows.append({'r_in': 3, 'L': 0, 'q_in': 1, 'mid': {'L': 1}})
    rows.append({'r_in': 6, 'L': 1, 'q_in': 0, 'mid': {'r_in': 2}})
    rows.append({'r_in': 1, 'L': 0, 'q_in': 1, 'mid': {'q_in': 0}})
    rows.append({'r_in': 4, 'L': 1, 'q_in': 1, 'mid': {'L': 0}})
    rows.append({'r_in': 2, 'L': 0, 'q_in': 0, 'mid': {'r_in': 7, 'L': 1}})
    while len(rows) < cycles:
        i = len(rows)
        r = rng.getrandbits(3)
        L = rng.getrandbits(1)
        q = rng.getrandbits(1)
        row = {'r_in': r, 'L': L, 'q_in': q}
        if i % 3 == 0:
            row['mid'] = {'L': rng.getrandbits(1)}
        elif i % 5 == 0:
            row['mid'] = {'r_in': rng.getrandbits(3)}
        elif i % 7 == 0:
            row['mid'] = {'q_in': rng.getrandbits(1)}
        elif i % 11 == 0:
            row['mid'] = {'L': rng.getrandbits(1), 'r_in': rng.getrandbits(3)}
        rows.append(row)
    return rows[:cycles]
