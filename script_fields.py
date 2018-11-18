"""
display questoions for each field type
validate data input for each field type
"""

def get_user_input(step, data):
    # Replace prompt with templated values
    prompt = step['prompt'].format(**data)
    data_type = step['type']

    field_data = input(prompt + '\n\n\t')
    print()
    return DATA_COLLECTION_FUNCS[data_type](prompt, step, data)

DATA_COLLECTION_FUNCS = {
    'text': lambda *args: foo(*args),
    'email': lambda *args: foo(*args),
    'multiple choice': lambda *args: foo(*args),
    'single choice': lambda *args: foo(*args),
    'boolean': lambda *args: foo(*args),
    'date': lambda *args: foo(*args),
    'info': lambda *args: foo(*args),
    'number': lambda *args: foo(*args),
}

def get_text(prompt, step, data):
    pass

def get_text(prompt, step, data):
    pass

def get_text(prompt, step, data):
    pass

def get_text(prompt, step, data):
    pass

def get_text(prompt, step, data):
    pass

def get_text(prompt, step, data):
    pass

def get_text(prompt, step, data):
    pass
