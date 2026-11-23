def reference(vectors):
    st = 0
    out = []
    for row in vectors:
        reset = row["reset"]
        data = row["data"]
        if reset:
            st = 0
        else:
            if st == 0:
                if data:
                    st = 1
            elif st == 1:
                st = 2 if data else 0
            elif st == 2:
                st = 2 if data else 3
            elif st == 3:
                st = 4 if data else 0
            elif st == 4:
                st = 4
        out.append({"start_shifting": 1 if st == 4 else 0})
    return out
