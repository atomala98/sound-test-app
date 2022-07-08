from time import time

def timer(func):
    def wrapper_function(*args, **kwargs):
        start = time()
        out = func(*args,  **kwargs)
        print(time() - start)
        return out
    return wrapper_function
