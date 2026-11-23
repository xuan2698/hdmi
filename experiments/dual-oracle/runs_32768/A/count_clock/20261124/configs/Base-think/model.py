def reference(vectors):
    hour=12
    minute=0
    second=0
    pm=0
    reset=0
    ena=0
    out=[]
    for row in vectors:
        if 'reset' in row:
            reset=row['reset']
        if 'ena' in row:
            ena=row['ena']
        if reset:
            hour=12
            minute=0
            second=0
            pm=0
        elif ena:
            second+=1
            if second==60:
                second=0
                minute+=1
                if minute==60:
                    minute=0
                    if hour==12:
                        hour=1
                    else:
                        hour+=1
                        if hour==12:
                            pm^=1
        out.append({
            'pm': pm&1,
            'hh': (((hour//10)<<4)|(hour%10))&0xff,
            'mm': (((minute//10)<<4)|(minute%10))&0xff,
            'ss': (((second//10)<<4)|(second%10))&0xff
        })
        for k,v in row.get('mid', {}).items():
            if k=='reset':
                reset=v
            elif k=='ena':
                ena=v
    return out
