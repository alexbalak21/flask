def decorator_with_args(decorator_arg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Pass the decorator argument to the decorated function
            return func(*args, decorator_arg=decorator_arg, **kwargs)
        return wrapper
    return decorator

@decorator_with_args("Hello from decorator!")
def example_function(x, decorator_arg=None):
    print(f"Function argument: {x}")
    print(f"Decorator argument: {decorator_arg}")

# Example usage
example_function(10)


def hello(func):                                                                                            
    def inner():                                                                                            
        print("Hello ")                                                                                     
        func()                                                                                              
    return inner                                                                                            