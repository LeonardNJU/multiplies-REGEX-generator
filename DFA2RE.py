from MyRE import MyRegex, Star

class Equation:
    def getName(num:int):   # _qi_ means REGEX which matches '01 strings' = i mod N
        return f"_q{num}_"
    def __init__(self,leftName:str,rightSide:dict):
        self.var=leftName
        self.r=rightSide
    def __str__(self):
        return self.var+ "="+ '|'.join([str(k) + str(v) for k,v in self.r.items()])


def show(eqs):
    for i in eqs:
        print(i)

def init(N):
    assert N%2      # now only generate REGEX which matches multiples of odd number
    eqs=[]
    for i in range(N):
        eqs.append(Equation(Equation.getName(i),{Equation.getName(i//2 if not i%2 else (i+N)//2 ):MyRegex('0'),Equation.getName((i-1)//2 if not (i-1)%2 else (i+N-1)//2):MyRegex('1')}))
    eqs[0].r['']=MyRegex('')
    return eqs

def eliminate(eqs,i,debug=False):
    if debug:print(f"Before: ",eqs[i])
    # eliminate eqs[i]
    curr=eqs[i]
    if curr.var in curr.r.keys():
        suf=curr.r.pop(curr.var)
        for k in curr.r.keys():
            curr.r[k]+=Star(suf)
    for otherEq in range(len(eqs)):
        if otherEq==i:
            continue
        if curr.var in eqs[otherEq].r.keys():
            suf=eqs[otherEq].r.pop(curr.var)
            for k in curr.r.keys():     # insert into otherEq with suffix
                if k in eqs[otherEq].r.keys():
                    eqs[otherEq].r[k]=eqs[otherEq].r[k]|(curr.r[k]+suf)
                else:
                    eqs[otherEq].r[k]=curr.r[k]+suf
    if debug:print(f"After: ",eqs[i])

def main():
    eqs=init(int(input("Enter N: ")))
    print("Initial Equations:")
    show(eqs)
    # now eliminate system of equations from bottom to top
    for i in range(len(eqs)-1,-1,-1):
        eliminate(eqs,i)
    # final sweet output
    print("\nFinal REGEX:")
    show(eqs)

if __name__ == '__main__':
    main()

