def stimulus(rng, cycles):
    rows = []
    reset = 1
    for i in range(cycles):
        if i < 2:
            reset = 1
        elif i < 4:
            reset = 0
        elif i == 4:
            reset = 1
        elif i == 5:
            reset = 0
        elif i == 6:
            reset = 1
        elif i < 10:
            reset = 0
        elif i == 10:
            reset = 1
        elif i < 14:
            reset = 0
        elif i == 14:
            reset = 1
        elif i < 20:
            reset = 0
        elif i == 20:
            reset = 1
        elif i < 24:
            reset = 0
        elif i == 24:
            reset = 1
        elif i < 30:
            reset = 0
        elif i == 30:
            reset = 1
        elif i < 40:
            reset = 0
        elif i == 40:
            reset = 1
        elif i < 50:
            reset = 0
        elif i == 50:
            reset = 1
        elif i < 60:
            reset = 0
        elif i == 60:
            reset = 1
        elif i < 70:
            reset = 0
        elif i == 70:
            reset = 1
        elif i < 80:
            reset = 0
        elif i == 80:
            reset = 1
        elif i < 100:
            reset = 0
        elif i == 100:
            reset = 1
        elif i < 120:
            reset = 0
        elif i == 120:
            reset = 1
        elif i < 150:
            reset = 0
        elif i == 150:
            reset = 1
        elif i < 200:
            reset = 0
        elif i == 200:
            reset = 1
        elif i < 250:
            reset = 0
        elif i == 250:
            reset = 1
        elif i < 300:
            reset = 0
        elif i == 300:
            reset = 1
        elif i < 400:
            reset = 0
        elif i == 400:
            reset = 1
        elif i < 500:
            reset = 0
        elif i == 500:
            reset = 1
        elif i < 700:
            reset = 0
        elif i == 700:
            reset = 1
        elif i < 1000:
            reset = 0
        elif i == 1000:
            reset = 1
        elif i < 1500:
            reset = 0
        elif i == 1500:
            reset = 1
        elif i < 2000:
            reset = 0
        elif i == 2000:
            reset = 1
        elif i < 3000:
            reset = 0
        elif i == 3000:
            reset = 1
        else:
            reset = 0
        rows.append({'reset': reset})
    return rows
