from rest_framework.exceptions import ValidationError


class LinkValid:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = 'youtube.com'
        temp_val = dict(value).get(self.field)
        if reg not in temp_val:
            raise ValidationError("wrong value")

