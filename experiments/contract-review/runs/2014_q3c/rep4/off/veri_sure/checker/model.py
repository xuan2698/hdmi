def reference(vectors):
    # Contract: combinational Moore FSM outputs sampled after posedge settles.
    # Y0 = LSB of next state Y; z = Moore output based on present state y.
    # Y0 = 1 iff (y[2]==0 and x==1) or (y==3'b011 and x==0) or (y==3'b100 and x==0)
    # z  = 1 iff y==3'b011 or y==3'b100
    out = []
    for row in vectors:
        y = row.get('y', 0) & 0x7
        x = row.get('x', 0) & 0x1
        y2 = (y >> 2) & 1
        if (y2 == 0 and x == 1) or (y == 0b011 and x == 0) or (y == 0b100 and x == 0):
            Y0 = 1
        else:
            Y0 = 0
        z = 1 if (y == 0b011 or y == 0b100) else 0
        out.append({'Y0': Y0, 'z': z})
    return out
