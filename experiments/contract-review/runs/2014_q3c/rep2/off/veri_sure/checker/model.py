def reference(vectors):
    # Contract: combinational Moore FSM outputs.
    # Y0 = 1 iff (y==0 and x==1) or (y==1 and x==0) or (y==2 and x==1) or (y==3 and x==0)
    # z  = 1 iff y==3 or y==4
    # Sample after posedge settled; mid changes occur after sampling.
    results = []
    for vec in vectors:
        y = vec['y'] & 0x7
        x = vec['x'] & 0x1
        Y0 = 1 if ((y == 0 and x == 1) or (y == 1 and x == 0) or
                   (y == 2 and x == 1) or (y == 3 and x == 0)) else 0
        z = 1 if (y == 3 or y == 4) else 0
        results.append({'Y0': Y0, 'z': z})
    return results
