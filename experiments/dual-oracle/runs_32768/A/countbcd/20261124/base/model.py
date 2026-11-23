def reference(vectors):
    q=0
    res=0
    out=[]
    for row in vectors:
        if 'reset' in row:
            res=row['reset']&1
        if res:
            q=0
        else:
            d0=q&15
            d1=(q>>4)&15
            d2=(q>>8)&15
            d3=(q>>12)&15
            d0+=1
            if d0==10:
                d0=0
                d1+=1
                if d1==10:
                    d1=0
                    d2+=1
                    if d2==10:
                        d2=0
                        d3+=1
                        if d3==10:
                            d3=0
            q=(d3<<12)|(d2<<8)|(d1<<4)|d0
        o=q&15
        t=(q>>4)&15
        h=(q>>8)&15
        e0=1 if o==9 else 0
        e1=1 if o==9 and t==9 else 0
        e2=1 if o==9 and t==9 and h==9 else 0
        ena=e0|(e1<<1)|(e2<<2)
        out.append({'q':q&65535,'ena':ena&7})
        if 'mid' in row:
            mid=row['mid']
            if 'reset' in mid:
                res=mid['reset']&1
    return out
