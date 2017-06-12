from formencode import htmlfill


defaults = {
    'name': 'Bob Jones',
    'occupation': 'Crazy Cultist',
    'address': '14 W. Canal\nNew Guinea',
    'living': 'no',
    'nice_guy': 0
}
errors ={
'occupation': 'Culivist is not allowed here.'
}
def mydefault_formatter(error):
    s="<ERROR>%s</ERROR>" % error
    return s

parser = htmlfill.FillingParser(
    defaults,
    errors,
    error_formatters={'myformatter':mydefault_formatter}
    )
parser.feed("""
<myform>
<form:error name="occupation" format="myformatter">
<input type="text" name="name" value="fill">
<select name="occupation">
<option value="">Default</option>
<option value="Crazy Cultist">Crazy cultist</option>
</select>

<textarea cols=20 style="width: 100%" name="address">An address</textarea>
<input type="radio" name="living" value="yes">
<input type="radio" name="living" value="no">
<input type="checkbox" name="nice_guy" checked="checked">
</myform>""")
parser.close()
print(parser.text())
