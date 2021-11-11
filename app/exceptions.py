class CoreException(Exception):
    pass


class InvalidConfiguration(CoreException):
    pass


class InvalidFilterPolicy(CoreException):
    pass


class DispatchPluginException(CoreException):
    pass
