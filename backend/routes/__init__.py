"""Expose individual routers for the application.

This package used to expose a single `api` router. The routes were split
into smaller modules (`admin_routes`, `user_routes`, `auth_routes`,
`user_registration`) — expose those routers here so callers can import
them from `backend.routes` without triggering import errors.
"""

from .admin_routes import router as admin_router
from .user_routes import router as user_router
from .auth_routes import router as auth_router
from .email_routes import router as email_router


__all__ = [
	"admin_router",
	"user_router",
	"auth_router",
	"email_router"
]
