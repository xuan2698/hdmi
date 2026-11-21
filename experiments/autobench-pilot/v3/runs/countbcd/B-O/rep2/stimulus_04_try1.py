def stimulus(rng, cycles):
    rows = []
    def row(reset):
        return {'reset': reset}
    rows.append(row(1))
    rows.append(row(0))
    for i in range(cycles - 2):
        if i < 8:
            rows.append(row(0))
        else:
            rows.append(row(rng.getrandbits(1)))
    return rows[:cycles]
