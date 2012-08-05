from __future__ import division

__author__ = "Marek Rudnicki"


import thorns
import waves
import dumpdb


import functools
import inspect
import sys


class _MapWrap(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, data):
        if isinstance(data, tuple):
            result = self.func(*data)

        elif isinstance(data, dict):
            result = self.func(**data)

        else:
            raise RuntimeError, "Arguments must be stored as tuple or dict."

        return result





def map(func, iterable, backend='serial'):


    if backend == 'serial':
        import __builtin__

        results = __builtin__.map(
            _MapWrap(func),
            iterable
        )

    if backend == 'multiprocessing':
        import multiprocessing

        pool = multiprocessing.Pool()

        results = pool.map(
            _MapWrap(func),
            iterable,
        )


    elif backend == 'joblib':
        import joblib


        def func_args_kwargs(func, data):
            if isinstance(data, tuple):
                out = (func, data, {})

            elif isinstance(data, dict):
                out = (func, (), data)

            else:
                raise RuntimeError, "Arguments must be stored as tuple or dict."

            return out



        results = joblib.Parallel(n_jobs=-1, verbose=100)(
            func_args_kwargs(func, i) for i in iterable
        )


    elif backend == 'pp':
        import pp


        def wrap(func, data):
            if isinstance(data, tuple):
                result = func(*data)
            elif isinstance(data, dict):
                result = func(**data)
            else:
                raise RuntimeError, "Arguments must be stored as tuple or dict."
            return result


        job_server = pp.Server( ppservers=("*",), ncpus=0 )

        modules = []
        depfuncs = []
        for k,v in func.func_globals.items():
            if inspect.ismodule(v):
                modules.append( "import " + v.__name__ + " as " + k )

            if inspect.isfunction(v):
                depfuncs.append(v)

        jobs = []
        for i in iterable:
            job = job_server.submit(
                func=wrap,
                args=(func,i),
                modules=tuple(modules),
                depfuncs=tuple(depfuncs),
                globals=func.func_globals
            )
            jobs.append(job)

        results = [job() for job in jobs]

    else:
        raise RuntimeError, "Unknown map() backend: {}".format(backend)



    return results
