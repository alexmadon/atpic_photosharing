import unittest

import atpic.sql_protocol

xml="""
<insert>
<table>mytable</table>
<field name="field1">value1</field>
<field name="field2"><b>important</b> text</field>
<field name="field3">joe's book</field>
<field name="int1">99999</field>
</insert>
"""

class protocol_test(unittest.TestCase):

    """html filter"""


    def test_insert(self):
        """insert"""
        sql=atpic.sql_protocol.insert(xml)





if __name__ == "__main__":
    unittest.main()
