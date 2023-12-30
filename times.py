class A:
    pass

class B(A):
    pass

class C(B):

    a: int
    b: int

    def __init__(self, **kwargs):
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')

c1 = C(a=5, b=6)

c1.__dict__.update(b=9)
print(c1.__dict__)
