#!/usr/bin/python3
# py3k version
"""Unit tests for URL dispatcher"""
import unittest
import urllib.parse
import io
import time
import atpic.tokenizer


class validate_test(unittest.TestCase):
    """Validate tests"""
    def test_validate_simple(self):

        alist=(
            ("个性化首页 · 网络历史记录","个 性 化 首 页 网 络 历 史 记 录"),
            ("alex","alex"),
            ("alex 个性化首页 · 网络历史记录","alex 个 性 化 首 页 网 络 历 史 记 录"),
            ("cet été là","cet ete la"),
            ("Garçon","garcon"),
            ("แล้วพบกันใหม่","แลว พบ กน ใหม"), # "แล้ว พบ กัน ใหม่"),
            ("私の名前は中野です","私 の 名前 は 中野 てす"), # "私 の 名前 は 中野 です"),
            ("alex madon 本日は晴天なり","alex madon 本日 は 晴天 なり"),
            ("HELLO!!?. My dear!","hello my dear"),
            ("(alex)madon","alex madon"),
            ("❰alex⟪madon","alex madon"),
            ("blanc-bec","blanc bec"),
            ("blanc‿bec","blanc bec"),
            ("blanc_bec","blanc bec"),

            ("天気ですね","天気 てす ね"), # kazu

            )
        i=0
        for (s,expected) in alist:
            i=i+1
            print('============',i,'==============')
            print(s)
            start = time.time()
            res=atpic.tokenizer.tokenize(s.encode('utf8'))
            elapsed = time.time() - start
            print('took:',elapsed)
            print('INPUT:',s)
            print('OUTPUT',res.decode('utf8'))
            print('EXPECTED',expected)
            print('XXX ("',s,'","',res.decode('utf8'),'"),',sep='')
            
            self.assertEqual(res.decode('utf8'),expected)


if __name__=="__main__":
    unittest.main()
