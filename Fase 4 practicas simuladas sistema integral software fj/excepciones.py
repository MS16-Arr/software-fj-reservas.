"""
Módulo de excepciones personalizadas.
Permite manejar errores específicos del sistema de reservas.
"""

class ErrorSoftwareFJ(Exception):
    """Excepción base para todos los errores de la aplicación."""
    pass


class ErrorCliente(ErrorSoftwareFJ):
    """Errores relacionados con datos inválidos de clientes."""
    pass


class ErrorServicio(ErrorSoftwareFJ):
    """Errores relacionados con servicios inválidos."""
    pass


class ErrorReserva(ErrorSoftwareFJ):
    """Errores relacionados con reservas."""
    pass