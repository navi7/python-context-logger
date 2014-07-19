# -*- coding: utf8 -*-
__author__ = 'ivanmesic@gmail.com'

__all__ = [
    'ContextLogger'
    'context_logger',
    'log_context',
    'JsonFormatter'
]

import json
import logging
from logging import (Logger,
                     Manager)


from functools import wraps

from context_logger import ContextLogger
from json_formatter import JsonFormatter

# attach logger
logging.setLoggerClass(ContextLogger)

_logging_patched = False


def _patch_logging():
    """
    Patch std logging so the root logger is in fact our ContextLogger
    :return:
    """
    global _logging_patched
    _logging_patched = True

    # replace the root with context logger
    logging.root = ContextLogger('root')
    Logger.root = logging.root
    Logger.manager = Manager(Logger.root)


if not _logging_patched:
    _patch_logging()

_common_fields = []


def common_names_filename(filename):
    global _common_fields
    try:
        with open(filename) as fields_file:
            _common_fields = json.load(fields_file)['common_fields']
    except Exception:
        pass  # nevermind



def log_context(prefix=None, **fields):
    """
    Adds all of the fields to the logging context for this call and expands them
    at the point of the call. If the variable is not available at that point in
    the method, it will be skipped.

    `fields` are set as name=value pairs where the name is the output name and
    the value is a _path_ for the variable. For example (class_method is a method
    in a class that is decorated with @context_logging):

    @log_context(external_id='event.externalId')
    def class_method(self, param1, ...):
        self.event = get_event()
        ...
        self.log.debug("A message")   # in the output there is an 'external_id': 'XYT' value
    """
    _fields = fields
    _prefix = prefix

    def decorator(func):
        _func = func

        @wraps(func)
        def _log_context(obj=None, *args, **kwargs):
            if obj and hasattr(obj, 'log'):
                if not obj.log.common_fields:
                    obj.log.common_fields = _common_fields

                obj.log.start_context(obj, _func.__name__, _prefix, _fields)
                return_value = _func(obj, *args, **kwargs)
                obj.log.end_context()
            else:
                root = logging.getLogger()
                if not root.common_fields:
                    root.common_fields = _common_fields
                root.start_context(_func, _func.func_name.lower(), _prefix, _fields)
                if obj is None:
                    return_value = _func(*args, **kwargs)
                else:
                    return_value = _func(obj, *args, **kwargs)
                root.end_context()

            return return_value

        return _log_context

    return decorator


def context_logger(name=None, prefix=None):
    """
    A decorator that adds ContextLogger object to class that it is applied to.

    After decorating the class, that class has a self.log variable to be used
    when logging.

    `prefix` is added to all logged variables that are not among `common_vars`.
    """
    def _context_log(klass):
        __orig_init = klass.__init__

        def new_init(self, *args, **kwargs):
            # attach the logger
            if name is None:
                class_name = self.__class__.__name__.lower()

            self.log = logging.getLogger(name or class_name)
            if not self.log.common_fields:
                self.log.common_fields = _common_fields

            self.log.start_context(klass, name or class_name, prefix, {})

            # do what you have to do
            __orig_init(self, *args, **kwargs)

        klass.__init__ = new_init
        return klass

    return _context_log