from foodgram.filters import Filter


class NameFilter(Filter):
    title = "имени"
    parameter_name = "username"


class EmailFilter(Filter):
    title = "e-mail"
    parameter_name = "email"
