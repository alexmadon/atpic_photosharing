#!/usr/bin/python3
import unittest
import atpic.normal

class normal_test(unittest.TestCase):
    """USER legacy urls"""

    def test_normal(self):
 
        inputs=(
            ("الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ","الحمد لله رب العالمين"), 
            ("الْعَرَبِيّةُ","العربية"), # stripTashkeel
            ("garçon","garcon"),
            ("été","ete"),
            ("العـــــربية","العربية"), # stripTatweel
            # ("لانها لالء الاسلام","لانها لالئ الاسلام"),  # normalizeLigature
            # Læsø
            ("samsø","samso"),
            ("Læsø","Laeso"),
            ("œuf","oeuf"),
            ("große","grosse"),
            ("niño","nino"),

)
        for (ain,aex) in inputs:  
            aout=atpic.normal.remove_diacritics(ain.encode('utf8'))
            aout=aout.decode('utf8')
            print(ain,'=>',aout)        
            self.assertEqual(aout,aex)


if __name__=="__main__":
    unittest.main()
