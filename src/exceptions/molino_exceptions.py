class MolinoException(Exception):
    """Excepción base del sistema (errores técnicos: BD, conexión, etc.)."""
    pass


class ValidacionDatosError(MolinoException):
    """Error de reglas de negocio o de datos ingresados por el operador."""
    pass
