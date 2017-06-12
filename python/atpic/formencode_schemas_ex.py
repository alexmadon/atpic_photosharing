import formencode

class UserAddress(formencode.Schema):
    allow_extra_fields = True
    validate_partial_form = True
    
    street = formencode.validators.String(not_empty=True)
    street_number = formencode.validators.Int(not_empty=True)
    street_number_suffix = formencode.validators.String(not_empty=True)
    postal_code = formencode.validators.String(not_empty=True)
    city = formencode.validators.String(not_empty=True)


class UserName(formencode.Schema):
    allow_extra_fields = True
    validate_partial_form = True
    
    firstname = formencode.validators.String(not_empty=True)
    surname_prefix = formencode.validators.String()
    surname = formencode.validators.String(not_empty=True)
    
class UserSignup(formencode.Schema):
    allow_extra_fields = True
    child_schemas = [UserAddress, UserName]
            
    def _to_python(self, value, state):
        errors = {}
        for schema_cls in self.child_schemas:
            schema = schema_cls()
            try:
                schema.to_python(value, state)
            except formencode.Invalid, error:
                formencode.schema.merge_dicts(errors, error.error_dict)

        if len(errors) > 0:
            raise formencode.Invalid(
                formencode.schema.format_compound_error(errors),
                value, state,
                error_dict=errors)            
    
