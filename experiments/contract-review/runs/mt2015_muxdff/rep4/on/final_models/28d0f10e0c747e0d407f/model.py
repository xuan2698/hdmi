def reference(vectors):
    # Q_posedge_update: At each posedge, Q becomes r_in when L=1; otherwise Q becomes q_in.
    Q = 0  # power-up unspecified; first posedge overwrites
    state = {"L": 0, "q_in": 0, "r_in": 0}
    out = []
    for row in vectors:
        # Input values before sampled edge
        if "L" in row:
            state["L"] = row["L"]
        if "q_in" in row:
            state["q_in"] = row["q_in"]
        if "r_in" in row:
            state["r_in"] = row["r_in"]
        # Q_posedge_update
        if state["L"]:
            Q = state["r_in"] & 1
        else:
            Q = state["q_in"] & 1
        out.append({"Q": Q})
        # Mid changes occur after sampling, before next edge; carry to next row.
        if "mid" in row:
            mid = row["mid"]
            try:
                if "signal" in mid and "value" in mid:
                    k = mid["signal"]
                    v = mid["value"]
                    if k == "L":
                        state["L"] = v
                    elif k == "q_in":
                        state["q_in"] = v
                    elif k == "r_in":
                        state["r_in"] = v
                else:
                    for k, v in mid.items():
                        if k == "L":
                            state["L"] = v
                        elif k == "q_in":
                            state["q_in"] = v
                        elif k == "r_in":
                            state["r_in"] = v
            except:
                try:
                    for entry in mid:
                        try:
                            if "signal" in entry and "value" in entry:
                                k = entry["signal"]
                                v = entry["value"]
                                if k == "L":
                                    state["L"] = v
                                elif k == "q_in":
                                    state["q_in"] = v
                                elif k == "r_in":
                                    state["r_in"] = v
                            else:
                                for k, v in entry.items():
                                    if k == "L":
                                        state["L"] = v
                                    elif k == "q_in":
                                        state["q_in"] = v
                                    elif k == "r_in":
                                        state["r_in"] = v
                        except:
                            try:
                                k = entry[0]
                                v = entry[1]
                                if k == "L":
                                    state["L"] = v
                                elif k == "q_in":
                                    state["q_in"] = v
                                elif k == "r_in":
                                    state["r_in"] = v
                            except:
                                try:
                                    k = entry[1]
                                    v = entry[2]
                                    if k == "L":
                                        state["L"] = v
                                    elif k == "q_in":
                                        state["q_in"] = v
                                    elif k == "r_in":
                                        state["r_in"] = v
                                except:
                                    pass
                except:
                    pass
    return out
