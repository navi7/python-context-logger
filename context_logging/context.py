
class Context(object):

    def __init__(self, obj, name, prefix, fields):
        self.name = name
        self.obj = obj
        self.fields = fields
        self.prefix = prefix

    def get_values(self):
        ctx = {}
        for field_name, value_field_name in self.fields.viewitems():
            field_value = self._unpack_value(value_field_name)
            if field_value is not None:
                ctx[field_name] = field_value
        return ctx

    def _unpack_value(self, field):
        """
        If that `field` can be found among the variables of the object, use that value.
        Otherwise, use the value.

        :param field_name: full field name (in dotted notation) or the value
        :return: value of the field or None if field is not present
        """
        if isinstance(field, basestring):
            parts = field.split('.')
            count = 0  # only if we manage to get all path parts, we are on the correct value
            curr_obj = self.obj
            for part in parts:
                if hasattr(curr_obj, part):
                    curr_obj = getattr(curr_obj, part)
                    count += 1

            if count == len(parts):
                # processed all elements so we are on the final element, return the value
                return curr_obj
            elif len(parts) == 1:
                return field
            return None

        # in case that is the only value and it's not class variable, return it
        return field


