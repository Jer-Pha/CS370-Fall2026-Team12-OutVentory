from decouple import config

from .base import *

if config("DEBUG", default=True, cast=bool):
    from .dev import *
else:
    from .prod import *
