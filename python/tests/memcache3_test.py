#!/usr/bin/python3
# py3k version
import atpic.memcached3 as mc
import unittest

con=mc.connect()
kv={
    "somekey1":"Some Value1",
    "somekey2":"Some Value2",
    "somekey3":"Clara cet été là",
    }
class memcachetest(unittest.TestCase):
    """USER legacy urls"""
    def testset(self):
        for key,value in kv.items():
            print(key,value)
            mc.set(con,key,value)
            value2=mc.get(con,key)
            self.assertEqual(value,value2)
    
    def testsets(self):
        for key,value in kv.items():
            print(key,value)
            mc.set(con,key,value)
        res=mc.gets(con,*(kv.keys()))
        print(res)
        res=mc.gets(con,"somekey1","somekey2","somekey3")
        print(res)

    def testdelete(self):

        mc.set(con,"key1","value1")
        val1=mc.get(con,"key1")
        self.assertEqual(val1,"value1")
        mc.delete(con,"key1")
        val2=mc.get(con,"key1")
        self.assertEqual(val2,None)

    
    def testincr(self):
        mc.set(con,"counter",0)
        counter=mc.increment(con,"counter")
        self.assertEqual(counter,1)
        mc.delete(con,"counter")

        counter2=mc.increment(con,"counter2")
        self.assertEqual(counter2,None)


if __name__=="__main__":
    unittest.main()
