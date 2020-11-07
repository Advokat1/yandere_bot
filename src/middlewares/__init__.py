from config.app import dp
from .ThrottlingMiddleware import ThrottlingMiddleware

__all__ = ['ThrottlingMiddleware']

dp.setup_middleware(ThrottlingMiddleware(.3))
