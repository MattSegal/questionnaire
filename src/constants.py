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
CONDITIONS = [
    'is',
    'is not',
    'contains', # (falls back to is)
    'not contains', # (falls back to is not)
    'is greater than', # (int)
    'is less than', # (int)
]
