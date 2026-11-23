def reference(vectors):
    N=8
    ev=eo=dv=do=0
    out=[]
    prev=None
    for i,r in enumerate(vectors):
        ip=None
        if 'edge' in r:
            e=r['edge']
            if isinstance(e,str):
                s=e.lower()
                ip=('pos' in s or s in ('1','true','rising'))
            else:
                ip=bool(e)
        if ip is None and 'clk_in' in r:
            c=r['clk_in']
            if prev is None:
                ip=(c==1)
            else:
                if prev==0 and c==1:
                    ip=True
                elif prev==1 and c==0:
                    ip=False
                else:
                    ip=(i%2==0)
            prev=c
        if ip is None:
            ip=(i%2==0)
        rst=r.get('rst_in',0)
        if rst==1:
            ev=eo=dv=do=0
        out.append({'enc_valid_out':ev,'enc_data_out':eo,'dec_valid_out':dv,'dec_data_out':do})
        if ip and not rst:
            ei=r.get('enc_valid_in',0)
            di=r.get('dec_valid_in',0)
            ev=1 if ei else 0
            dv=1 if di else 0
            x=r.get('enc_data_in',0)
            y=0
            for j in range(N):
                p=1 if ((x>>j)&1) else 2
                y |= p << (2*j)
            eo=y
            x=r.get('dec_data_in',0)
            y=0
            for j in range(N):
                p=(x>>(2*j))&3
                if p==1:
                    y |= 1<<j
            do=y
    return out
