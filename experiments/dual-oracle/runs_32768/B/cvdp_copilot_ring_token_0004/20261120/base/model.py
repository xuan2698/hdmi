def reference(vectors):
    state = 0
    token_received = 1
    token = 0
    data_out = 0
    results = []
    
    for i, row in enumerate(vectors):
        rst = row.get('rst', 0)
        data_in = row.get('data_in', 0) & 0xF
        has_data = row.get('has_data_to_send', 0)
        
        if 'clk' in row:
            is_posedge = (row['clk'] == 1)
        else:
            is_posedge = (i % 2 == 0)
        
        if rst:
            state = 0
            token_received = 1
            token = 0
            data_out = 0
            reset_active = True
        else:
            reset_active = False
        
        results.append({
            'data_out': data_out & 0xF,
            'token_received': token_received & 0xF,
            'token': token & 0xF
        })
        
        if is_posedge and not reset_active:
            if state == 0:
                token_received = 2
                token = 1
                data_out = data_in if has_data else 0
                state = 1
            elif state == 1:
                token_received = 4
                token = 2
                data_out = data_in if has_data else 0
                state = 2
            elif state == 2:
                token_received = 8
                token = 4
                data_out = data_in if has_data else 0
                state = 3
            elif state == 3:
                token_received = 1
                token = 8
                data_out = data_in if has_data else 0
                state = 0
            else:
                state = 0
                token_received = 1
                token = 0
                data_out = 0
                
    return results
