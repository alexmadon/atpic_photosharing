# -*- coding: utf-8 -*-
import atpic.database


import unittest

class pg_test(unittest.TestCase):
    """Test postgresql triggers functions"""

    con=atpic.database.connect()

    def DEPREC_testPyclean(self):
        """Extract text from HTML"""
        
        
        text_html="""alex is the <b>best</b>"""
        text_txt_expected="""alex is the best"""
        query="SELECT pyclean('%s')" % text_html
        result=atpic.database.query(query, self.con)
        text_txt=result[0]['pyclean']
        
        self.assertEqual(text_txt_expected,text_txt)

    def DEPREC_testPycleanUnicode(self):
        """Extract text with accents Unicode utf8"""
        
        
        text_html="""cet été"""
        text_txt_expected="""cet été"""
        query="SELECT pyclean('%s')" % text_html
        result=atpic.database.query(query, self.con)
        text_txt=result[0]['pyclean']
        
        self.assertEqual(text_txt_expected,text_txt)


    def DEPREC_testPycleanEntity(self):
        """Extract text with accents Unicode utf8"""
        
        
        text_html="""Alex &amp; Dama"""
        text_txt_expected="""Alex &amp; Dama"""
        query="SELECT pyclean('%s')" % text_html
        result=atpic.database.query(query, self.con)
        text_txt=result[0]['pyclean']
        
        self.assertEqual(text_txt_expected,text_txt)





    def DEPREC_testPycleanNull(self):
        """Extract NULL"""
        
        
        text_txt_expected=''
        query="SELECT pyclean(NULL)"
        result=atpic.database.query(query, self.con)
        text_txt=result[0]['pyclean']
        self.assertEqual(text_txt_expected,text_txt)

    def DEPREC_testPycleanDropComments(self):
        """Extract text from HTML drop comments"""
        
        
        text_html="""alex is the <b>best</b><!-- comment --> ok"""
        text_txt_expected="""alex is the best ok"""
        query="SELECT pyclean('%s')" % text_html
        result=atpic.database.query(query, self.con)
        text_txt=result[0]['pyclean']
        
        self.assertEqual(text_txt_expected,text_txt)

    def testStateFunction(self):
        """Tests sum_solr_state_function"""
        
        query="""SELECT sum_solr_state_function('an already long string',ROW(1,'a',1,999,'test'))"""
        result=atpic.database.query(query, self.con)
        col_got=result[0]['sum_solr_state_function']
        col_expected="""an already long string<field name="tagger">1</field><field name="tag">test</field>"""
        
        self.assertEqual(col_expected,col_got)





if __name__ == "__main__":
    unittest.main()
