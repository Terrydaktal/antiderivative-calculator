from threading import Thread
from functools import wraps

def timeout(timeout:int) -> (tuple, dict):
    def decorator(func) -> (tuple, dict):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Exception:
            err = [Exception('function [{}] timeout [{} seconds] exceeded!'.format(func.__name__, timeout))]

            def theFunc() -> None:
                try:
                    err[0] = func(*args, **kwargs)
                except Exception as e:
                    err[0] = e

            thread = Thread(target=theFunc)
            thread.daemon = True
            try:
                thread.start()
                thread.join(timeout)
            except Exception as ex:
                print ('error starting thread')	
                raise ex
            retval = err[0]
            if isinstance(retval, BaseException):
                raise retval
            return retval

        return wrapper

    return decorator
