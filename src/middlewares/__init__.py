from config.app import dp
from .ThrottlingMiddleware import ThrottlingMiddleware
from .ValidateUserMiddleware import ValidateUserMiddleware

__all__ = ['ThrottlingMiddleware', ]

dp.setup_middleware(ThrottlingMiddleware(.3))
dp.setup_middleware(ValidateUserMiddleware())
