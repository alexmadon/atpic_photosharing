import formencode


class UserForm(formencode.Schema):
    username=formencode.validators.PlainText(not_empty=True)
    age=formencode.validators.Int(not_empty=True)
    email=formencode.validators.Email()


def TestInput(InputDict):
    schema=UserForm()
    print "====TESTING===="
    try:
        form_data = schema.to_python(InputDict)
        print "OK:"
        print str(form_data)
    except formencode.Invalid, error:
        print "Error:"
        print "errorvalue %s" % error.value
        print str(error.error_dict)
        print str(error.error_list)
        print error


# TestInput({'username':'99.23','age':'102'})
# TestInput({'username':'bob','age':'102'})
# print formencode.validators.PlainText(not_empty=True).all_messages()
