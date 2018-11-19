from .fields import get_user_input


def execute(script):
    """
    Executes the script then returns data
    """
    data = {f: None for f in script['data_fields']}
    step_name = script['start']
    while step_name:
        step_name = run_step(step_name, script, data)

    return data


def run_step(step_name, script, data):
    """
    Runs a single step of the questionnaire,
    also runs any follow questions, as specified by 'details'
    """
    print(step_name)
    step = script['steps'].get(step_name)
    if not step:
        return

    response = get_user_input(step, data)
    if step_name in script['data_fields']:
        data[step_name] = response

    # Execute any follow up details in a depth-first manner.
    details = step.get('details', [])
    for detail in details:
        if evaluate_when(detail['when'], data):
            detail_step_name = detail['then']
            while detail_step_name:
                detail_step_name = run_step(detail_step_name, script, data)

    next_step_name = None
    then = step.get('then')
    if type(then) is str:
        return then
    elif type(then) is list:
        return get_then_from_options(then, data)



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
    if type(var) is list:
        return val in var
    else:
        return val == var
