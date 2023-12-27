def timer(fn):
    from time import perf_counter
    import logging

    def inner(*args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        logging.info('{0} took {1:.8f}s to execute'.format(fn.__name__, execution_time))
        return to_execute

    return inner
