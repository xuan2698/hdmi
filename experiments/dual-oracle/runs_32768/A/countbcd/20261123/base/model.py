def reference(vectors):
    q=0
    cur=0
    out=[]
    for row in vectors:
        if 'reset' in row:
            cur=row['reset']
        if cur:
            q=0
        else:
            d=[q&15,(q>>4)&15,(q>>8)&15,(q>>12)&15]
            i=0
            while i<4:
                if d[i]==9:
                    d[i]=0
                    i+=1
                else:
                    d[i]+=1
                    break
            q=d[0]|(d[1]<<4)|(d[2]<<8)|(d[3]<<12)
        ones=q&15
        tens=(q>>4)&15
        hun=(q>>8)&15
        e1=1 if ones==9 else 0
        e2=1 if (e1 and tens==9) else 0
        e3=1 if (e2 and hun==9) else 0
        ena=e1|(e2<<1)|(e3<<2)
        out.append({'ena':ena,'q':q})
        if 'mid' in row:
            mid=row['mid']
            if 'reset' in mid:
                cur=mid['reset']
    return out
