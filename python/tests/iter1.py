class MySeq:
    def __init__(self, *data):
        self.data = data
    def __iter__(self):
        print "call __iter__1"
        return MySeqIterator(self.data)

class MySeqIterator:
    def __init__(self, data):
        self.index = 0
        self.data = data
    def next(self):
        print "call next()"
        if self.index < len(self.data):
            item = self.data[self.index]
            self.index += 1 # ready for next call
            return item
        else: # out of bounds
            raise StopIteration



obj = MySeq(1, 9, 3, 4)
for item in obj:
    print item
