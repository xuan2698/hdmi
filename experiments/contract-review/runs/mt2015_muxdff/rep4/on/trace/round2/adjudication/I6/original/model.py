def reference(vectors):
    # Q_posedge_update: At each posedge, after settlement, Q becomes r_in when L=1; otherwise Q becomes q_in.
    # No reset: power-up state is concretely chosen as Q=0 for this reference model.
    Q = 0
    L = 0
    q_in = 0
    r_in = 0
    out = []
    for row in vectors:
        # Drive row values before the sampled posedge edge.
        try:
            L = row["L"]
        except:
            pass
        try:
            q_in = row["q_in"]
        except:
            pass
        try:
            r_in = row["r_in"]
        except:
            pass
        # Q_posedge_update: registered update at posedge after settlement.
        if L:
            Q = 1 if r_in else 0
        else:
            Q = 1 if q_in else 0
        out.append({"Q": Q})
        # Mid changes occur after sampling, before the other edge, and carry to the next row start.
        try:
            mid = row["mid"]
        except:
            mid = None
        if mid is not None:
            try:
                for key, val in mid.items():
                    if key == "L":
                        L = val
                    elif key == "q_in":
                        q_in = val
                    elif key == "r_in":
                        r_in = val
            except:
                try:
                    for change in mid:
                        try:
                            for key, val in change.items():
                                if key == "L":
                                    L = val
                                elif key == "q_in":
                                    q_in = val
                                elif key == "r_in":
                                    r_in = val
                        except:
                            try:
                                key = change[0]
                                val = change[1]
                                if key == "L":
                                    L = val
                                elif key == "q_in":
                                    q_in = val
                                elif key == "r_in":
                                    r_in = val
                            except:
                                pass
                except:
                    pass
    return out
