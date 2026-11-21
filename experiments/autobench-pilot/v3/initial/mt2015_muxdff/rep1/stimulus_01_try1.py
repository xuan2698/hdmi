def stimulus(rng, cycles):
    rows = []
    rows.append({'r': 0, 'L': 1, 'clk': 0})
    rows.append({'r': 7, 'L': 1, 'clk': 0})
    rows.append({'r': 0, 'L': 0, 'clk': 0})
    rows.append({'r': 5, 'L': 0, 'clk': 0, 'mid': {'clk': 1}})
    rows.append({'r': 3, 'L': 1, 'clk': 0, 'mid': {'clk': 1}})
    rows.append({'r': 6, 'L': 0, 'clk': 0})
    rows.append({'r': 1, 'L': 0, 'clk': 0, 'mid': {'clk': 1}})
    rows.append({'r': 2, 'L': 1, 'clk': 0})
    rows.append({'r': 4, 'L': 0, 'clk': 0, 'mid': {'clk': 1}})
    rows.append({'r': 7, 'L': 0, 'clk': 0})
    rows.append({'r': 0, 'L': 1, 'clk': 0, 'mid': {'clk': 1}})
    rows.append({'r': 3, 'L': 0, 'clk': 0})
    while len(rows) < cycles:
        r = rng.getrandbits(3)
        L = rng.getrandbits(1)
        row = {'r': r, 'L': L, 'clk': 0}
        if rng.random() < 0.5:
            row['mid'] = {'clk': 1}
        rows.append(row)
    return rows[:cycles]
