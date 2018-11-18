"""
TODO - parse spec into something we can execute using a *simple* question engine
ie. we want to try handle any complexity or weirdness here

- parse when fields
"""
from constants import FIELD_KEYS, FIELD_TYPES, CONDITIONS


def parse(spec):
    """
    Parse the spec into a script that can be executed
    """
    fields = set(spec.keys())
    script = {
        'start': None,
        'data': {field: None for field in fields},
        'steps': {},
    }
    # Fill out steps
    for field in fields:
        step = {}
        for key, val in spec[field].items():
            if key in ('details', 'then') and type(val) is list:
                element = {}
                for el in val:
                    element['then'] = el['then']
                    # Parse 'when' fields
                    when = el.get('when')
                    if not when:
                        continue

                    fragments = when.split(' ')
                    variable = fragments[0]
                    condition = None
                    condition_and_value = ' '.join(fragments[1:])
                    for c in CONDITIONS:
                        if c == condition_and_value[0:len(c)]:
                            condition = c

                    value = condition_and_value[len(condition):].strip()
                    element['when'] = {
                        'variable': variable,
                        'condition': condition,
                        'value': value
                    }
            else:
                step[key] = val

        script['steps'][field] = step
        # Check for start field
        if spec[field].get('start'):
            script['start'] = field

    return script
