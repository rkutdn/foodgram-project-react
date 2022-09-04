from foodgram.filters import Filter


class NameFilter(Filter):
    title = "названию"
    parameter_name = "name"


class UsernameFilter(Filter):
    title = "имени автора"
    parameter_name = "author__username"


class TagnameFilter(Filter):
    title = "названию тега"
    parameter_name = "tags__name"
