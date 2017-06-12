class Parent:
    def doall(self):
        self.get()
    def get(self):
        print "A"


class Child(Parent):
    def get(self):
        print "B"




mya=Parent()
myb=Child()

mya.doall()
myb.doall()
