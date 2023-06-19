from drawzero.utils.i18n import I18N


class BadDrawParmsError(Exception):
    def __init__(self, errors=None, call_string='', example=''):
        self.errors = errors or []
        self.call_string = call_string
        self.example = example

    def __str__(self):
        errors_list_string = '\n'.join(self.errors)
        return f'\n{self.call_string}\n{errors_list_string}\n{I18N.example}\n{self.example}'

    def finish(self):
        super().__init__(self.__str__())
