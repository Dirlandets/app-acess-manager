import os

try:
    PRODUCTION = os.environ.get('ENV') in ['PROD', ]
except KeyError:
    PRODUCTION = False

if PRODUCTION:
    print('PROD')
    from .production import *  # noqa: F403,F401
else:
    print('DEVELOP')
    from .develop import *  # noqa: F403,F401
