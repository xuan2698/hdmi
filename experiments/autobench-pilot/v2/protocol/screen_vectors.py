def screen_vectors(rng, cycles, widths, resets):
    result = []
    for cycle in range(cycles):
        sample = {}
        for name, width in widths.items():
            if name in resets:
                if cycle == 0:
                    sample[name] = resets[name]
                else:
                    if rng.random() < 1.0 / 32.0:
                        sample[name] = resets[name]
                    else:
                        sample[name] = 1 - resets[name]
            else:
                if width <= 0:
                    sample[name] = 0
                else:
                    sample[name] = rng.getrandbits(width)
        result.append(sample)
    return result
