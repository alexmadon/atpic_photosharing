# ttserver test.tct

from pyrant import Tyrant, Q
t = Tyrant(host='127.0.0.1', port=1978)
t['i'] = {'name': 'Martin Conte Mac Donell', 'gender': 'M', 'age': 26}
t['you'] = {'name': 'Guido', 'gender': 'M', 'age': 33}    
print t['i']
{'name': 'Martin Conte Mac Donell', 'gender': 'M'}
