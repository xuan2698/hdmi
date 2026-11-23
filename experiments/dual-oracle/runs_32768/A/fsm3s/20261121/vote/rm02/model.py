def reference(vectors):
    state = 0
    result = []
    for row in vectors:
        if row["reset"]:
            state = 0
        else:
            inp = row["in"]
            if state == 0:
                state = 1 if inp else 0
            elif state == 1:
                state = 1 if inp else 2
            elif state == 2:
                state = 3 if inp else 0
            else:
                state = 1 if inp else 2
        result.append({"out": 1 if state == 3 else 0})
    return result
