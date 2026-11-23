def reference(vectors):
    state = "IDLE"
    ciphertext = 0
    done = 0
    sums = [0, 0, 0]
    results = []
    for idx, row in enumerate(vectors):
        reset = int(row.get("reset", 0)) & 1
        start = int(row.get("start", 0)) & 1
        plaintext = int(row.get("plaintext", 0)) & 0x7FFF
        key = int(row.get("key", 0)) & ((1 << 45) - 1)

        if "edge" in row:
            e = row["edge"]
            if isinstance(e, str):
                posedge = e.lower().startswith("p") or e == "1"
            else:
                posedge = (e == 1)
        elif "clk" in row:
            posedge = (int(row["clk"]) == 1)
        else:
            posedge = (idx % 2 == 0)

        results.append({"ciphertext": ciphertext, "done": done})

        if not posedge:
            continue

        if reset:
            state = "IDLE"
            ciphertext = 0
            done = 0
            sums = [0, 0, 0]
        else:
            if state == "IDLE":
                done = 0
                if start:
                    state = "COMPUTE"
                else:
                    state = "IDLE"
            elif state == "COMPUTE":
                p0 = plaintext & 0x1F
                p1 = (plaintext >> 5) & 0x1F
                p2 = (plaintext >> 10) & 0x1F

                k0 = key & 0x1F
                k1 = (key >> 5) & 0x1F
                k2 = (key >> 10) & 0x1F
                k3 = (key >> 15) & 0x1F
                k4 = (key >> 20) & 0x1F
                k5 = (key >> 25) & 0x1F
                k6 = (key >> 30) & 0x1F
                k7 = (key >> 35) & 0x1F
                k8 = (key >> 40) & 0x1F

                sums[0] = p0 * k0 + p1 * k1 + p2 * k2
                sums[1] = p0 * k3 + p1 * k4 + p2 * k5
                sums[2] = p0 * k6 + p1 * k7 + p2 * k8

                state = "COMPUTE_MOD"
                done = 0
            elif state == "COMPUTE_MOD":
                c0 = sums[0] % 26
                c1 = sums[1] % 26
                c2 = sums[2] % 26
                ciphertext = (c0 & 0x1F) | ((c1 & 0x1F) << 5) | ((c2 & 0x1F) << 10)
                done = 1
                state = "DONE"
            elif state == "DONE":
                done = 0
                state = "IDLE"

    return results
