def reference(vectors):
    out=0
    prev=0
    cur={'reset':0,'in':0}
    r=[]
    for row in vectors:
        if 'reset' in row: cur['reset']=row['reset']
        if 'in' in row: cur['in']=row['in']
        rst=cur['reset']&1
        inv=cur['in']&0xffffffff
        if rst:
            out=0
        else:
            out=(out|(prev&(~inv)&0xffffffff))&0xffffffff
        prev=inv
        r.append({'out':out&0xffffffff})
        m=row.get('mid')
        if isinstance(m,dict):
            for k,v in m.items():
                if k in cur: cur[k]=v
    return r
