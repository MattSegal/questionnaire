FIELD_KEYS = {
    'start',
    'prompt',
    'options',
    'help',
    'details',
    'then',
}
FIELD_TYPES = {
    'text',
    'email',
    'multiple choice',
    'single choice',
    'boolean',
    'date',
    'info',
    'number',
}
TYPE_VALIDATORS = {
    'multiple choice': lambda *args: validate_choice_field(*args),
    'single choice':  lambda *args: validate_choice_field(*args),
}
CONDITIONS = [
    'is',
    'is not',
    'contains', # (falls back to is)
    'not contains', # (falls back to is not)
    'is greater than', # (int)
    'is less than', # (int)
]


def validate(spec):
    fields = set(spec.keys())

    errors = []
    num_starts = 0
    start_fields = set()

    def add_error(msg, *args):
        if args:
            errors.append(msg.format(*args))
        else:
            errors.append(msg)

    for field in fields:
        field_spec = spec[field]

        # Check for the start field
        if field_spec.get('start'):
            num_starts += 1
            start_fields.add(field)

        # Field must have a prompt
        if not field_spec.get('prompt'):
            add_error('{} must have a prompt', field)

        # Field must have a type
        if not field_spec.get('type'):
            add_error('{} must have a type', field)
        # Field type must be valid
        elif field_spec['type'] not in FIELD_TYPES:
            add_error('{}\'s type \'{}\' is not valid, must be one of {}', field, field_spec['type'], FIELD_TYPES)
        else:
            # Apply any type validations
            validate_type = TYPE_VALIDATORS.get(field)
            if validate_type:
                validate_type(field, field_spec, add_error)

        # All keys should be in whitelist
        undefined_keys = set(field_spec.keys()) -  FIELD_KEYS
        if not undefined_keys:
            add_error('{} cannot have keys {}, must be one of {}', field, undefined_keys, FIELD_KEYS)

        # Help must be a string if it is present
        help_text = field_spec.get('help')
        if help_text and type(help_text) is not str:
            add_error('{}\'s help text must be text', field)

        validate_details(field, field_spec, fields, add_error)
        validate_then(field, field_spec, fields, add_error)

    # There should be one start field
    if num_starts > 1:
        add_error('There should be only one start field, found {}: {}', num_starts, start_fields)
    elif num_starts < 1:
        add_error('There should be at least one start field, found none')

    return errors


def validate_details(field, field_spec, fields, add_error):
    """
    The "details" field
        - must be a list
        - for each element
    """
    details = field_spec.get('details')
    if not details:
        return
    elif type(details) is not list:
         add_error('{}\'s \'details\' field should be a list')
    elif type(details) is list:
        for element in details:
            validate_conditional_then(element, 'details', field, field_spec, fields, add_error)


def validate_then(field, field_spec, fields, add_error):
    """
    The "then" field
        - may be a string or a list
        - if a string, must be a question name
        - if a list see rules for details
    """
    then = field_spec.get('then')
    if not then:
        return
    elif not ((type(then) is str) or (type(then) is list)):
        add_error('{}\'s \'then\' field should be text or a list', field)
    elif type(then) is str and then not in fields:
        add_error('{}\'s \'then\' field is {}, but it must be one of {}', then, fields)
    elif type(then) is list:
        for element in then:
            validate_conditional_then(element, 'then', field, field_spec, fields, add_error)


def validate_conditional_then(element, key_name, field, field_spec, fields, add_error):
    """
    A conditional then:
        - must have a then field which is a field name
        - may a when, which must have form "VARIABLE CONDITION VALUE"
            - value may be an integer, "string", True False
            - variable must be a question name
            - condition must be one of CONDITIONS
    """
    then = element.get('then')
    when = element.get('when')
    if not then:
        add_error('Each element of {}\'s \'{}\' field must have a \'then\' field', field, key_name)
    if not then in fields:
        add_error('Each element of {}\'s \'{}\' field must have a \'then\' field which is one of {}', field, key_name, fields)
    if when:
        def when_formatting_error():
            add_error('Each element of {}\'s \'{}\' field must have a \'when\' field which has the form \'VARIABLE CONDITION VALUE\'')

        fragments = when.split(' ')
        if not len(fragments) > 2:
            when_formatting_error()
            return

        variable = fragments[0]
        if not variable in fields:
            add_error('Each element of {}\'s \'{}\' field must have a \'when\' field has a variable in {}', field, key_name, fields)
            return

        condition_and_value = ' '.join(fragments[1:])
        condition = None
        for c in CONDITIONS:
            if c == condition_and_value[0:len(c)]:
                condition = c

        if not condition:
            add_error('Each element of {}\'s \'{}\' field must have a \'when\' field which contains one of these conditions {}', field, key_name, CONDITIONS)
            return

        value = condition_and_value[len(condition):].strip()
        if not value:
            when_formatting_error()
            return

        # TODO - validate value by field type
        # - boolean must be in True, False
        # - number must be a number
        # - greater / less than must be number


def validate_choice_field(field, field_spec, add_error):
    """
    Ensure the field has an options key,
    which should be a list and each option should be truthy
    """
    options = field_spec.get('options')
    if not options:
        add_error('{} should have an options field', field)
    elif not type(options) is list or not all(options):
        add_error('{} should be a list of options', field)
