def reference(vectors):
    ss_ones=0; ss_tens=0; mm_ones=0; mm_tens=0; hh_ones=2; hh_tens=1; pm_state=0
    out=[]
    for v in vectors:
        reset=v['reset']; ena=v['ena']
        if reset:
            ss_ones=0; ss_tens=0; mm_ones=0; mm_tens=0; hh_ones=2; hh_tens=1; pm_state=0
        elif ena:
            ss_ones+=1
            if ss_ones==10:
                ss_ones=0; ss_tens+=1
                if ss_tens==6:
                    ss_tens=0; mm_ones+=1
                    if mm_ones==10:
                        mm_ones=0; mm_tens+=1
                        if mm_tens==6:
                            mm_tens=0
                            hh_ones+=1
                            if hh_tens==1 and hh_ones==3:
                                hh_tens=0; hh_ones=1; pm_state^=1
                            elif hh_tens==0 and hh_ones==10:
                                hh_tens=1; hh_ones=0
                            elif hh_tens==1 and hh_ones==10:
                                hh_tens=0; hh_ones=1; pm_state^=1
        hh=hh_tens*16+hh_ones; mm=mm_tens*16+mm_ones; ss=ss_tens*16+ss_ones
        out.append({'pm':pm_state,'hh':hh,'mm':mm,'ss':ss})
    return out