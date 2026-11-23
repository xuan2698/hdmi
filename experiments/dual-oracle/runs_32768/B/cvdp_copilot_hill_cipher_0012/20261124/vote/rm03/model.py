def reference(vectors):
    def is_posedge(edge):
        if isinstance(edge, str):
            e = edge.lower()
            return e.startswith("pos") or e in ("1", "rise", "rising", "posedge")
        return edge == 1 or edge is True

    if isinstance(vectors, dict):
        if "vectors" in vectors:
            vectors = vectors["vectors"]
        else:
            vectors = [vectors]

    state = 0  # 0=IDLE, 1=COMPUTE, 2=COMPUTE_MOD, 3=DONE
    ciphertext = 0
    latched_plain = 0
    latched_key = 0

    cur_reset = 0
    cur_start = 0
    cur_plaintext = 0
    cur_key = 0

    mask45 = (1 << 45) - 1
    out = []

    for row in vectors:
        if isinstance(row, dict):
            if "reset" in row:
                cur_reset = int(row["reset"]) & 1
            if "start" in row:
                cur_start = int(row["start"]) & 1
            if "plaintext" in row:
                cur_plaintext = int(row["plaintext"]) & 0x7fff
            if "key" in row:
                cur_key = int(row["key"]) & mask45

        out.append({
            "ciphertext": ciphertext & 0x7fff,
            "done": 1 if state == 3 else 0
        })

        edge = row.get("edge", 0) if isinstance(row, dict) else 0

        if is_posedge(edge):
            if cur_reset:
                state = 0
                ciphertext = 0
                latched_plain = 0
                latched_key = 0
            else:
                if state == 0:
                    if cur_start:
                        latched_plain = cur_plaintext
                        latched_key = cur_key
                        state = 1
                elif state == 1:
                    state = 2
                elif state == 2:
                    p0 = latched_plain & 31
                    p1 = (latched_plain >> 5) & 31
                    p2 = (latched_plain >> 10) & 31

                    k0 = latched_key & 31
                    k1 = (latched_key >> 5) & 31
                    k2 = (latched_key >> 10) & 31
                    k3 = (latched_key >> 15) & 31
                    k4 = (latched_key >> 20) & 31
                    k5 = (latched_key >> 25) & 31
                    k6 = (latched_key >> 30) & 31
                    k7 = (latched_key >> 35) & 31
                    k8 = (latched_key >> 40) & 31

                    c0 = (p0 * k0 + p1 * k1 + p2 * k2) % 26
                    c1 = (p0 * k3 + p1 * k4 + p2 * k5) % 26
                    c2 = (p0 * k6 + p1 * k7 + p2 * k8) % 26

                    ciphertext = (c0 & 31) | ((c1 & 31) << 5) | ((c2 & 31) << 10)
                    state = 3
                elif state == 3:
                    state = 0

    return out
