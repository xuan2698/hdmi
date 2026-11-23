def reference(vectors):
    out1 = out2 = out3 = 0
    results = []
    
    def to_signed(v):
        if isinstance(v, str):
            v = int(v, 0) if v.startswith('0x') else int(v)
        v = v & 0xFFFF
        if v >= 0x8000:
            v -= 0x10000
        return v
    
    for i, row in enumerate(vectors):
        # Determine edge type
        if 'edge' in row:
            e = row['edge']
            posedge = (e == 'posedge' or e == 1 or e == '1' or e is True)
        elif 'clk' in row:
            c = row['clk']
            posedge = (c == 1 or c == '1' or c is True)
        else:
            posedge = (i % 2 == 0)
        
        # Asynchronous active-high reset
        rst = row.get('reset', 0)
        if isinstance(rst, str):
            rst = int(rst, 0) if rst.startswith('0x') else int(rst)
        if rst:
            out1 = out2 = out3 = 0
        
        # Read outputs before NBA updates
        results.append({
            'out_1': out1 & 0xFFFF,
            'out_2': out2 & 0xFFFF,
            'out_3': out3 & 0xFFFF
        })
        
        # Update on posedge if not in reset
        if posedge and not rst:
            sel = row.get('filter_select', 0)
            if isinstance(sel, str):
                sel = int(sel, 0) if sel.startswith('0x') else int(sel)
            sel = sel & 0x3
            
            in1 = to_signed(row.get('in_1', 0))
            in2 = to_signed(row.get('in_2', 0))
            in3 = to_signed(row.get('in_3', 0))
            
            out1 = out1 + ((in1 - out1) >> sel)
            out2 = out2 + ((in2 - out2) >> sel)
            out3 = out3 + ((in3 - out3) >> sel)
            
            if out1 > 32767: out1 = 32767
            elif out1 < -32768: out1 = -32768
            if out2 > 32767: out2 = 32767
            elif out2 < -32768: out2 = -32768
            if out3 > 32767: out3 = 32767
            elif out3 < -32768: out3 = -32768
    
    return results
