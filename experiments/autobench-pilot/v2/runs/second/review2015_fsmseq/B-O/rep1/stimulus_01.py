def stimulus(rng, cycles):
    out = []
    state = 0
    found = False
    for i in range(cycles):
        reset = 0
        data = 0
        if i == 0:
            reset = 1
            data = rng.getrandbits(1)
        elif i == 1:
            reset = 1
            data = rng.getrandbits(1)
        elif i == 2:
            reset = 0
            data = 1
        elif i == 3:
            reset = 0
            data = 1
        elif i == 4:
            reset = 0
            data = 0
        elif i == 5:
            reset = 0
            data = 1
        elif i == 6:
            reset = 0
            data = rng.getrandbits(1)
        elif i == 7:
            reset = 1
            data = rng.getrandbits(1)
        elif i == 8:
            reset = 0
            data = 1
        elif i == 9:
            reset = 0
            data = 1
        elif i == 10:
            reset = 0
            data = 1
        elif i == 11:
            reset = 0
            data = 1
        elif i == 12:
            reset = 0
            data = 0
        elif i == 13:
            reset = 0
            data = 1
        elif i == 14:
            reset = 0
            data = 1
        elif i == 15:
            reset = 0
            data = 0
        elif i == 16:
            reset = 0
            data = 1
        elif i == 17:
            reset = 0
            data = 1
        elif i == 18:
            reset = 0
            data = 0
        elif i == 19:
            reset = 0
            data = 1
        elif i == 20:
            reset = 0
            data = 1
        elif i == 21:
            reset = 0
            data = 0
        elif i == 22:
            reset = 0
            data = 1
        elif i == 23:
            reset = 0
            data = 1
        elif i == 24:
            reset = 0
            data = 0
        elif i == 25:
            reset = 0
            data = 1
        elif i == 26:
            reset = 0
            data = 1
        elif i == 27:
            reset = 0
            data = 0
        elif i == 28:
            reset = 0
            data = 1
        elif i == 29:
            reset = 0
            data = 1
        elif i == 30:
            reset = 0
            data = 0
        elif i == 31:
            reset = 0
            data = 1
        elif i == 32:
            reset = 0
            data = 1
        elif i == 33:
            reset = 0
            data = 0
        elif i == 34:
            reset = 0
            data = 1
        elif i == 35:
            reset = 0
            data = 1
        elif i == 36:
            reset = 0
            data = 0
        elif i == 37:
            reset = 0
            data = 1
        elif i == 38:
            reset = 0
            data = 1
        elif i == 39:
            reset = 0
            data = 0
        elif i == 40:
            reset = 0
            data = 1
        elif i == 41:
            reset = 0
            data = 1
        elif i == 42:
            reset = 0
            data = 0
        elif i == 43:
            reset = 0
            data = 1
        elif i == 44:
            reset = 0
            data = 1
        elif i == 45:
            reset = 0
            data = 0
        elif i == 46:
            reset = 0
            data = 1
        elif i == 47:
            reset = 0
            data = 1
        elif i == 48:
            reset = 0
            data = 0
        elif i == 49:
            reset = 0
            data = 1
        elif i == 50:
            reset = 0
            data = 1
        elif i == 51:
            reset = 0
            data = 0
        elif i == 52:
            reset = 0
            data = 1
        elif i == 53:
            reset = 0
            data = 1
        elif i == 54:
            reset = 0
            data = 0
        elif i == 55:
            reset = 0
            data = 1
        elif i == 56:
            reset = 0
            data = 1
        elif i == 57:
            reset = 0
            data = 0
        elif i == 58:
            reset = 0
            data = 1
        elif i == 59:
            reset = 0
            data = 1
        elif i == 60:
            reset = 0
            data = 0
        elif i == 61:
            reset = 0
            data = 1
        elif i == 62:
            reset = 0
            data = 1
        elif i == 63:
            reset = 0
            data = 0
        elif i == 64:
            reset = 0
            data = 1
        elif i == 65:
            reset = 0
            data = 1
        elif i == 66:
            reset = 0
            data = 0
        elif i == 67:
            reset = 0
            data = 1
        elif i == 68:
            reset = 0
            data = 1
        elif i == 69:
            reset = 0
            data = 0
        elif i == 70:
            reset = 0
            data = 1
        elif i == 71:
            reset = 0
            data = 1
        elif i == 72:
            reset = 0
            data = 0
        elif i == 73:
            reset = 0
            data = 1
        elif i == 74:
            reset = 0
            data = 1
        elif i == 75:
            reset = 0
            data = 0
        elif i == 76:
            reset = 0
            data = 1
        elif i == 77:
            reset = 0
            data = 1
        elif i == 78:
            reset = 0
            data = 0
        elif i == 79:
            reset = 0
            data = 1
        elif i == 80:
            reset = 0
            data = 1
        elif i == 81:
            reset = 0
            data = 0
        elif i == 82:
            reset = 0
            data = 1
        elif i == 83:
            reset = 0
            data = 1
        elif i == 84:
            reset = 0
            data = 0
        elif i == 85:
            reset = 0
            data = 1
        elif i == 86:
            reset = 0
            data = 1
        elif i == 87:
            reset = 0
            data = 0
        elif i == 88:
            reset = 0
            data = 1
        elif i == 89:
            reset = 0
            data = 1
        elif i == 90:
            reset = 0
            data = 0
        elif i == 91:
            reset = 0
            data = 1
        elif i == 92:
            reset = 0
            data = 1
        elif i == 93:
            reset = 0
            data = 0
        elif i == 94:
            reset = 0
            data = 1
        elif i == 95:
            reset = 0
            data = 1
        elif i == 96:
            reset = 0
            data = 0
        elif i == 97:
            reset = 0
            data = 1
        elif i == 98:
            reset = 0
            data = 1
        elif i == 99:
            reset = 0
            data = 0
        else:
            reset = 1 if rng.random() < 0.05 else 0
            data = rng.getrandbits(1)
        out.append({'reset': reset, 'data': data})
    return out
