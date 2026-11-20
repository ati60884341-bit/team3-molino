from typing import List
from models.muestra_arroz_model import MuestraArrozModel
from models.entities.muestra_arroz import MuestraArroz
from exceptions.molino_exceptions import MolinoException, ValidacionDatosError

# Umbrales de humedad del escenario asignado (Molinos de Lambayeque - secado de arroz)
HUMEDAD_MINIMA_IDEAL = 12.0
HUMEDAD_MAXIMA_IDEAL = 14.0


class MuestraArrozController:
    """Controlador que orquesta la lógica de negocio para las Muestras de Arroz."""

    def __init__(self):
        self._modelo_muestra = MuestraArrozModel()

    def obtener_todas(self) -> List[MuestraArroz]:
        """Solicita al DAO la lista íntegra de muestras registradas."""
        try:
            return self._modelo_muestra.listar_todos()
        except MolinoException as error:
            raise error
        except Exception as error_inesperado:
            raise MolinoException(f"Falla inesperada al listar muestras: {error_inesperado}")

    def buscar_muestras(self, criterio_ingresado: str) -> List[MuestraArroz]:
        """Sanitiza el criterio de búsqueda y consulta al DAO."""
        try:
            criterio_limpio = criterio_ingresado.strip() if criterio_ingresado else ""
            return self._modelo_muestra.buscar_por_criterio(criterio_limpio)
        except MolinoException as error:
            raise error
        except Exception as error_inesperado:
            raise MolinoException(f"Falla inesperada al buscar muestras: {error_inesperado}")

    def registrar_muestra(self, lote: str, variedad: str, humedad_texto: str):
        """Valida la entrada del operador, registra la muestra y evalúa la alerta.

        Retorna una tupla (id_generado, mensaje_alerta) para que la Vista
        muestre el resultado exacto que exige el escenario.
        """
        lote_limpio = lote.strip() if lote else ""
        variedad_limpia = variedad.strip() if variedad else ""

        if not lote_limpio:
            raise ValidacionDatosError("Debe ingresar el código de lote.")
        if not variedad_limpia:
            raise ValidacionDatosError("Debe ingresar la variedad del arroz.")

        try:
            humedad_valor = float(humedad_texto.replace(",", "."))
        except (ValueError, AttributeError, TypeError):
            raise ValidacionDatosError("La humedad del grano debe ser un número (ejemplo: 13.5).")

        if humedad_valor < 0 or humedad_valor > 100:
            raise ValidacionDatosError("La humedad del grano debe estar entre 0% y 100%.")

        id_generado = self._modelo_muestra.registrar(lote_limpio, variedad_limpia, humedad_valor)
        mensaje_alerta = self.evaluar_alerta_humedad(humedad_valor)
        return id_generado, mensaje_alerta

    @staticmethod
    def evaluar_alerta_humedad(humedad_grano: float) -> str:
        """Regla de negocio del escenario: clasifica la humedad del grano en 3 rangos.

        < 12.0%        -> grano muy seco (riesgo de quiebre en el pilado)
        12.0% - 14.0%   -> humedad ideal para pilado
        > 14.0%         -> riesgo de hongos en los silos
        """
        if humedad_grano < HUMEDAD_MINIMA_IDEAL:
            return "GRANO MUY SECO - RIESGO DE QUIEBRE"
        elif humedad_grano > HUMEDAD_MAXIMA_IDEAL:
            return "ALERTA: RIESGO DE HONGOS"
        else:
            return "HUMEDAD IDEAL PARA PILADO"
