def reference(vectors):
    state = "A"
    inputs = {"areset": 0, "x": 0}
    out = []
    for row in vectors:
        # Apply row values driven before sampled edge
        for k, v in row.items():
            if k != "mid":
                inputs[k] = v

        # Sample after posedge settled; areset active-low
        if inputs["areset"] == 0:
            # reset_async_z0: areset==0 at any time; async reset forces state A and z=0
            state = "A"
            z = 0
        else:
            # Normal operation (areset==1)
            x = inputs["x"]
            if state == "A":
                if x == 0:
                    # A_x0_to_A_z0: areset==1, state A, x==0 -> next A, z=0
                    state = "A"
                    z = 0
                else:
                    # A_x1_to_C_z1: areset==1, state A, x==1 -> next C, z=1
                    state = "C"
                    z = 1
            elif state == "B":
                if x == 0:
                    # B_x0_to_C_z1: areset==1, state B, x==0 -> next C, z=1
                    state = "C"
                    z = 1
                else:
                    # B_x1_to_B_z0: areset==1, state B, x==1 -> next B, z=0
                    state = "B"
                    z = 0
            else:  # state == "C"
                if x == 0:
                    # C_x0_to_C_z1: areset==1, state C, x==0 -> next C, z=1
                    state = "C"
                    z = 1
                else:
                    # C_x1_to_B_z0: areset==1, state C, x==1 -> next B, z=0
                    state = "B"
                    z = 0

        out.append({"z": z})

        # Process mid changes after sampling, before other edge
        mid = row.get("mid", None)
        if mid:
            # Apply mid changes; support dict or list of dicts
            try:
                for k, v in mid.items():
                    inputs[k] = v
            except:
                for ch in mid:
                    for k, v in ch.items():
                        inputs[k] = v
            # Asynchronous reset may assert due to mid areset change
            if inputs["areset"] == 0:
                # reset_async_z0: asynchronous reset forces state A
                state = "A"

    return out
