def reference(vectors):
    # Rule q_posedge_update: At each sampled posedge, if r==1 then q becomes 0; otherwise q becomes d.
    # Between posedge events q holds its value. Synchronous active-high reset is implemented here.
    q = 0
    d = 0
    r = 0
    outputs = []
    for row in vectors:
        # Apply row inputs driven before the sampled posedge.
        if 'd' in row:
            d = row['d'] & 1
        if 'r' in row:
            r = row['r'] & 1
        # Posedge update: synchronous reset has priority.
        if r == 1:
            q = 0
        else:
            q = d & 1
        outputs.append({'q': q & 1})
        # Process optional mid changes AFTER sampling, before next clock edge.
        # These changes are carried to the start of the next row and do not affect current q.
        mid = row.get('mid', None)
        if mid:
            try:
                # Case: mid is a dict of input changes.
                for k, v in mid.items():
                    if k == 'd':
                        d = v & 1
                    elif k == 'r':
                        r = v & 1
            except:
                # Case: mid is a list of change dictionaries.
                try:
                    for change in mid:
                        for k, v in change.items():
                            if k == 'd':
                                d = v & 1
                            elif k == 'r':
                                r = v & 1
                except:
                    pass
    return outputs
