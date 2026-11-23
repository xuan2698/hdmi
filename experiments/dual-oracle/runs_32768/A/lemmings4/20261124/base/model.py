def reference(vectors):
 st=0;cnt=0
 cur={'areset':0,'bump_left':0,'bump_right':0,'ground':0,'dig':0}
 out=[]
 for row in vectors:
  mid=row.get('mid')
  for k in cur:
   if k in row:
    v=row[k]
    if k=='areset' and v==1 and cur[k]==0: st=0;cnt=0
    cur[k]=v
  if cur['areset']==1: st=0;cnt=0
  else:
   bl=cur['bump_left'];br=cur['bump_right'];g=cur['ground'];dg=cur['dig']
   if st==6: pass
   elif st in (0,1):
    if g==0: st=2 if st==0 else 3;cnt=1
    elif dg: st=4 if st==0 else 5;cnt=0
    else:
     if bl and br: st=1 if st==0 else 0
     elif bl: st=1
     elif br: st=0
     cnt=0
   elif st in (2,3):
    if g==1:
     if cnt>20: st=6
     else: st=0 if st==2 else 1
     cnt=0
    else: cnt+=1
   elif st in (4,5):
    if g==0: st=2 if st==4 else 3;cnt=1
    else: cnt=0
  if st==0: o={'walk_left':1,'walk_right':0,'aaah':0,'digging':0}
  elif st==1: o={'walk_left':0,'walk_right':1,'aaah':0,'digging':0}
  elif st in (2,3): o={'walk_left':0,'walk_right':0,'aaah':1,'digging':0}
  elif st in (4,5): o={'walk_left':0,'walk_right':0,'aaah':0,'digging':1}
  else: o={'walk_left':0,'walk_right':0,'aaah':0,'digging':0}
  out.append(o)
  if mid:
   for k,v in mid.items():
    if k=='areset' and v==1 and cur.get(k,0)==0: st=0;cnt=0
    cur[k]=v
 return out
