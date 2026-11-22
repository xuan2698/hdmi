def reference(vectors):
    # State encoding: START, INV0, INV1.
    state = "START"
    z = 0
    areset = 0
    x = 0
    outputs = []

    for row in vectors:
        # Apply row inputs before the sampled posedge.
        if "areset" in row:
            areset = row["areset"] & 1
        if "x" in row:
            x = row["x"] & 1

        # R_RESET: active-high asynchronous reset returns state to START.
        # Selected interpretation: z holds its previous value instead of forcing 0.
        if areset == 1:
            state = "START"

        # Posedge sampling.
        if areset == 1:
            # R_RESET: reset asserted; conversion stopped, z holds previous value.
            pass
        else:
            # R_CONVERT: 2's complement serial conversion, LSB first.
            if state == "START":
                if x == 0:
                    state = "START"
                    z = 0
                else:
                    state = "INV1"
                    z = 1
            elif state == "INV0":
                if x == 0:
                    state = "INV1"
                    z = 1
                else:
                    state = "INV0"
                    z = 0
            else:  # INV1
                if x == 0:
                    state = "INV1"
                    z = 1
                else:
                    state = "INV0"
                    z = 0

        outputs.append({"z": z & 1})

        # Mid-row changes occur after sampling and carry toward the next edge.
        if "mid" in row and row["mid"] is not None:
            mid = row["mid"]
            if "areset" in mid:
                areset = mid["areset"] & 1
            if "x" in mid:
                x = mid["x"] & 1

            # R_RESET: asynchronous reset assertion while mid changes occur.
            # Selected interpretation: state returns to START, z holds previous value.
            if areset == 1:
                state = "START"

    return outputs
