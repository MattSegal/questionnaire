from .fields import get_user_input


def execute(script):
    """
    Executes the script then returns data
    """
    data = {f: None for f in script['data_fields']}
    step_name = script['start']
    step = script['steps'][step_name]

    while step:
        response = get_user_input(step, data)
        if step_name in script['data_fields']:
            data[step_name] = response

        # TODO - details

        step_name = None
        then = step.get('then')
        if type(then) is str:
            step_name = then
        elif type(then) is list:
            step_name = get_then_from_options(then, data)

        step = script['steps'].get(step_name)

    return data


def get_then_from_options(then, data):
    conditional_options = [el for el in then if el.get('when')]
    unconditional_options = [el for el in then if not el.get('when')]
    for option in conditional_options:
        if evaluate_when(option['when'], data):
            return option['then']

    for option in unconditional_options:
        return option['then']


def evaluate_when(when, data):
    """
    Returns True if when condition is met.
    """
    variable = data.get(when['variable'])
    condition = when['condition']
    value = when['value']
    condition_func = CONDITION_FUNCS[condition]
    return condition_func(variable, value)


CONDITION_FUNCS = {
    'is': lambda var, val: var == val,
    'is not': lambda var, val: var != val,
    'contains': lambda var, val: contains(var, val),
    'not contains': lambda var, val: not contains(var, val),
    'is greater than': lambda var, val: int(var) > int(val),
    'is less than': lambda var, val: int(var) < int(val),
}

def contains(var, val):
    if type(val) is list:
        return var in val
    else:
        return var == val
