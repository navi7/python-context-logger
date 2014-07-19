import logging

from datetime import datetime

from context import Context


class ContextLogger(logging.Logger):
    """
    Holds the context for current logging. Adds all of the variables in all active
    contexts ti the log record
    """

    def __init__(self, name, common_fields=None):
        super(ContextLogger, self).__init__(name)
        self._common_fields = common_fields if common_fields else []
        self._contexts = list()
        self._prefix = None

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value

    @property
    def common_fields(self):
        return self._common_fields

    @common_fields.setter
    def common_fields(self, value):
        self._common_fields = value

    def start_context(self, obj, name, prefix, fields):
        self._contexts.append(Context(obj=obj, name=name, prefix=prefix, fields=fields))

    def end_context(self):
        self._contexts.pop()

    def add_to_context(self, *args, **kwargs):
        self._contexts[-1].fields.update(kwargs)

    def get_current_values(self):
        """
        Extracts the values from all of the contexts.
        :return: a dict of name, value pairs in all contexts
        """
        ctx = {}
        for context in self._contexts:
            ctx.update(self._apply_prefix(context.prefix or self.prefix, **context.get_values()))

        if len(self._contexts) > 0:
            try:
                class_name = str(self._contexts[-1].obj.__class__)
                if not class_name.startswith('<type \'function\''):
                    ctx['module_name'] = class_name.replace("<class '", '').replace("'>", '')
                ctx['func_name'] = self._contexts[-1].name  # this is set to func name
                ctx['timestamp'] = str(datetime.utcnow())
            except Exception:
                pass
        return ctx

    def _apply_prefix(self, prefix, **kwargs):
        """
        Updates argument names to include prefix if one is defined
        :param kwargs:
        :return:
        """
        updated = {}
        for key, val in kwargs.iteritems():
            if key in self._common_fields:
                new_key = key
            else:
                new_key = "{}_{}".format(prefix, key) if prefix else key
            updated[new_key] = val
        return updated

    def _log(self, level, msg, args, exc_info=None, extra=None, **kwargs):
        ctx_values = self.get_current_values()

        # currently active prefix
        prefix = self._contexts[-1].prefix if len(self._contexts) > 0 else self.prefix
        if 'extra' in kwargs:
            kwargs['extra'] = self._apply_prefix(prefix, **kwargs['extra'])
            kwargs['extra'].update(ctx_values)
        elif len(kwargs) > 0:
            if 'exc_info' in kwargs:
                kwargs = {'exc_info': kwargs.pop('exc_info'),
                          'extra': self._apply_prefix(prefix, **kwargs)}
            else:
                kwargs = {'extra': self._apply_prefix(prefix, **kwargs)}
            kwargs['extra'].update(ctx_values)
        elif ctx_values:
            kwargs['extra'] = ctx_values

        if extra is not None:
            if 'extra' in kwargs:
                kwargs['extra'].update(extra)
            else:
                kwargs['extra'] = extra

        # yank the status and put it into the `extra`
        if 'status' in kwargs:
            kwargs['extra']['status'] = kwargs['status']
            del kwargs['status']

        super(ContextLogger, self)._log(level, msg, args, **kwargs)

    #
    # HELPER methods for some standard status stuff:
    #  OK, ERROR, CREATED, UPDATED, NOOP, BLOCKED, REJECTED, FAIL

    # status field values
    OK = 'OK'
    ERROR = 'ERROR'
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    NOOP = 'NOOP'
    BLOCKED = 'BLOCKED'
    REJECTED = 'REJECTED'
    FAIL = 'FAIL'

    def ok(self, msg, *args, **kwargs):
        kwargs['status'] = self.OK
        self._log(logging.INFO, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        kwargs['status'] = self.ERROR
        self._log(logging.ERROR, msg, args, **kwargs)

    def created(self, msg, *args, **kwargs):
        kwargs['status'] = self.CREATED
        self._log(logging.INFO, msg, args, **kwargs)

    def updated(self, msg, *args, **kwargs):
        kwargs['status'] = self.UPDATED
        self._log(logging.INFO, msg, args, **kwargs)

    def noop(self, msg, *args, **kwargs):
        kwargs['status'] = self.NOOP
        self._log(logging.INFO, msg, args, **kwargs)

    def blocked(self, msg, *args, **kwargs):
        kwargs['status'] = self.BLOCKED
        self._log(logging.INFO, msg, args, **kwargs)

    def rejected(self, msg, *args, **kwargs):
        kwargs['status'] = self.REJECTED
        self._log(logging.INFO, msg, args, **kwargs)

    def fail(self, msg, *args, **kwargs):
        kwargs['status'] = self.FAIL
        self._log(logging.ERROR, msg, args, **kwargs)
