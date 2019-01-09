def smart_function():
    try:
        smart_function.counter += 1
    except AttributeError:
        smart_function.counter = 1
    return smart_function.counter
