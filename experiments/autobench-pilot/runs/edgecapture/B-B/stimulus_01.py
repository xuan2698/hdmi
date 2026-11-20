def stimulus(rng, cycles):
    result = [
        {"reset": 1, "in": 0xFFFFFFFF},
        {"reset": 1, "in": 0x00000000},
        {"reset": 0, "in": 0xFFFFFFFF},
        {"reset": 0, "in": 0xFFFFFFFF},
        {"reset": 0, "in": 0x00000000},
        {"reset": 0, "in": 0xFFFFFFFF},
        {"reset": 0, "in": 0x00000000},
        {"reset": 0, "in": 0xFFFFFFFF},
        {"reset": 0, "in": 0x55555555},
        {"reset": 0, "in": 0xAAAAAAAA},
        {"reset": 0, "in": 0x55555555},
        {"reset": 0, "in": 0xAAAAAAAA},
        {"reset": 0, "in": 0xF0F0F0F0},
        {"reset": 1, "in": 0x00000000},
        {"reset": 1, "in": 0xFFFFFFFF},
        {"reset": 0, "in": 0x00000000},
        {"reset": 0, "in": 0xFFFFFFFF},
        {"reset": 0, "in": 0x00000000},
        {"reset": 0, "in": 0x0F0F0F0F},
        {"reset": 0, "in": 0xF0F0F0F0},
    ]
    result = result[:cycles]
    while len(result) < cycles:
        reset_v = 1 if rng.random() < 0.05 else 0
        mode = rng.randrange(4)
        if mode == 0:
            val = rng.getrandbits(32)
        elif mode == 1:
            val = 0xFFFFFFFF
        elif mode == 2:
            val = 0x00000000
        else:
            val = rng.choice([0x55555555, 0xAAAAAAAA, 0xF0F0F0F0, 0x0F0F0F0F])
        result.append({"reset": reset_v, "in": val})
    return result
