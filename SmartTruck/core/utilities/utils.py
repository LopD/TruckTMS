'''
Any simple functions that can be used throughout the project.
'''


def str_to_bool(str_value: str | None) -> bool | None:
    '''
    Returns bool if it fits any of the given str choices.
    Returns None otherwise.
    '''
    choices = {
        "true":["true", "yes", "1"], 
        "false":["false", "no", "0"]
    }
    if str_value is None or not isinstance(str_value,str):
        return None
    str_value = str_value.lower()
    if str_value in choices['true']:
        return True
    elif str_value in choices['false']:
        return False
    return None



from django.db import connection, reset_queries

class QueryLogger:
    def __enter__(self):
        reset_queries()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for q in connection.queries:
            print(q["sql"], q["time"])

