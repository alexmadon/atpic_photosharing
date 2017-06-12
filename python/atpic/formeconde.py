import formencode
from formencode import validators
class SecurePassword(formencode.FancyValidator):
    words_filename = '/usr/share/dict/words'
    def _to_python(self, value, state):
        f = open(self.words_filename)
        lower = value.strip().lower()
        for line in f:
            if line.strip().lower() == lower:
                raise formencode.Invalid(
                    'Please do not base your password on a '
                    'dictionary term', value, state)
            return value
        
        
class Registration(formencode.Schema):
    """ The schema"""
    first_name = validators.String(not_empty=True)
    last_name = validators.String(not_empty=True)
    email = validators.Email(resolve_domain=True)
    username = formencode.All(validators.PlainText(),
                              UniqueUsername())
    password = SecurePassword()
    password_confirm = validators.String()
    chained_validators = [validators.FieldsMatch(
            'password', 'password_confirm')]
