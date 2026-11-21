def stimulus(rng, cycles):
    rows = []
    state = {"rst": 1, "data_in": 0, "has_data_to_send": 0}
    for i in range(cycles):
        if i < 3:
            state["rst"] = 1
            state["data_in"] = 0
            state["has_data_to_send"] = 0
        else:
            state["rst"] = 0
            r = rng.random()
            if r < 0.15:
                state["has_data_to_send"] = 0
                state["data_in"] = rng.randrange(16)
            elif r < 0.55:
                state["has_data_to_send"] = 1
                state["data_in"] = rng.randrange(16)
            else:
                state["has_data_to_send"] = rng.randrange(2)
                state["data_in"] = rng.randrange(16)
        row = {
            "rst": state["rst"],
            "data_in": state["data_in"] & 0xF,
            "has_data_to_send": state["has_data_to_send"] & 0x1,
        }
        if rng.random() < 0.3:
            mid = {
                "rst": state["rst"],
                "data_in": rng.randrange(16),
                "has_data_to_send": rng.randrange(2),
            }
            row["mid"] = mid
            state["data_in"] = mid["data_in"]
            state["has_data_to_send"] = mid["has_data_to_send"]
        rows.append(row)
    return rows
