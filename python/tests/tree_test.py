# -*- coding: utf-8 -*-
import unittest
import atpic.tree


class tree_asci2xml_test(unittest.TestCase):
    # class cleaner_test():
    """tree ASCII to XML"""
    
    
    def test_tree_basic(self):
        """a basic tree (no PID)"""

        thetext="""\
g12\n\n
 g23
 g34
g1
 g2
  g34



"""
        xml_expected="""\
<tree>
<gallery id="12"/>
<child>
<gallery id="23"/>
<gallery id="34"/>
</child>
<gallery id="1"/>
<child>
<gallery id="2"/>
<child>
<gallery id="34"/>
</child>
</child>
</tree>"""
        xml_found=atpic.tree.parse_txt(thetext)

        self.assertEqual(xml_found,xml_expected)
        
        
    def test_tree_pic(self):
        """a basic tree with PID"""

        thetext="""\
g12\n\n
 g23 p999
 g34
g1
 g2
  g34



"""
        xml_expected="""\
<tree>
<gallery id="12"/>
<child>
<gallery id="23" pid="999"/>
<gallery id="34"/>
</child>
<gallery id="1"/>
<child>
<gallery id="2"/>
<child>
<gallery id="34"/>
</child>
</child>
</tree>"""
        xml_found=atpic.tree.parse_txt(thetext)

        self.assertEqual(xml_found,xml_expected)
        
        
        
class tree_xml_test(unittest.TestCase):
    # class cleaner_test():
    """tree ASCII to XML"""
    
    
    def test_tree_gid(self):
        """extract GID"""

        xml="""\
<tree>
<gallery id="12"/>
<child>
<gallery id="23"/>
<gallery id="34"/>
</child>
<gallery id="1"/>
<child>
<gallery id="2"/>
<child>
<gallery id="34"/>
</child>
</child>
</tree>"""
        gid_list=atpic.tree.extract_gid_from_xml(xml)
        gid_list_expected=["12","23","34","1","2","34"]
        self.assertEqual(gid_list,gid_list_expected)
        
    def test_tree_pid(self):
        """extract PID"""

        xml="""\
<tree>
<gallery id="12"/>
<child>
<gallery id="23" pid="999"/>
<gallery id="34"/>
</child>
<gallery id="1"/>
<child>
<gallery id="2" pid="888"/>
<child>
<gallery id="34"/>
</child>
</child>
</tree>"""
        pid_list=atpic.tree.extract_pid_from_xml(xml)
        pid_list_expected=["","999","","","888",""]
        self.assertEqual(pid_list,pid_list_expected)
        
        
if __name__ == "__main__":
    unittest.main()
