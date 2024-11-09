class MyRegex:
    def __init__(self,re):
        if re in [None,'']:
            self.re=''
            self.empty=True
        else:
            self.re=str(re)
            self.empty=False
    def __str__(self):
        return self.re
    def __add__(self, other):
        res=self.empty_then_other(other)
        if res:return res
        else:
            if (isinstance(self,Star) and self.re==other) :
                return self
            if (isinstance(other,Star) and other.re==self):
                return other
            return Concat(self,other)
    def __or__(self, other):
        res=self.empty_then_other(other)
        if res:return res
        else:
            if (isinstance(self,Star) and self.re==other) :
                return self
            elif (isinstance(other,Star) and other.re==self):
                return other
            if isinstance(self,Concat) and self.r==other and isinstance(self.l,Star):
                return self
            elif isinstance(other,Concat) and other.r==self and isinstance(other.l,Star):
                return other
            return Union(self,other)
    def __eq__(self, other):
        return str(self)==str(other)
    def star(self):
        return Star(self)
    def empty_then_other(self,other):
        if self.empty:
            return other
        if other.empty:
            return self
        return None
    def with_brackets(self):
        return str(self)[0]=='(' and str(self)[-1]==')'
    # def empty(self):
    #     return self.empty

class Concat(MyRegex):
    def __init__(self,re1,re2):
        self.l=re1
        self.r=re2
        self.empty=self.l.empty or self.r.empty
    def __str__(self):
        return str(self.l)+str(self.r)

class Union(MyRegex):
    def __init__(self,re1,re2):
        self.l=re1
        self.r=re2
        self.empty=self.l.empty and self.r.empty
    def __str__(self):
        return '('+str(self.l)+'|'+str(self.r)+')'
    def with_empty_ret_not_null(self):
        if self.l.empty:return self.r
        if self.r.empty:return self.l
        return None

class Star(MyRegex):
    def __init__(self,re):
        self.re=re
        self.empty=re.empty
    def __str__(self):
        if isinstance(self.re,Union):
            maybeNull=self.re.with_empty_ret_not_null()
            if maybeNull:self.re=maybeNull
        if len(str(self.re))==1 or self.re.with_brackets():return str(self.re)+'*'
        return '('+str(self.re)+')*'