from typing import List
from database.conexion_bd import ConexionBD
from models.entities.muestra_arroz import MuestraArroz
from exceptions.molino_exceptions import MolinoException, ValidacionDatosError


class MuestraArrozModel:
    """Capa DAO: responsable exclusivo de la persistencia de las Muestras de Arroz."""

    @staticmethod
    def _mapear_filas(filas) -> List[MuestraArroz]:
        return [
            MuestraArroz(
                id_muestra=fila['id_muestra'],
                lote=fila['lote'],
                variedad=fila['variedad'],
                humedad_grano=float(fila['humedad_grano']),
                registrado_en=fila['registrado_en']
            )
            for fila in filas
        ]

    @staticmethod
    def listar_todos() -> List[MuestraArroz]:
        """Ejecuta 'sp_muestras_listar' y retorna la colección completa de muestras."""
        conexion = None
        cursor = None
        try:
            conexion = ConexionBD.obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            cursor.callproc('sp_muestras_listar')

            lista_muestras: List[MuestraArroz] = []
            for resultado in cursor.stored_results():
                lista_muestras.extend(MuestraArrozModel._mapear_filas(resultado.fetchall()))
            return lista_muestras

        except Exception as error_persistencia:
            raise MolinoException(f"Error en la capa DAO al listar muestras: {error_persistencia}")

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def buscar_por_criterio(criterio: str) -> List[MuestraArroz]:
        """Ejecuta 'sp_muestras_buscar' con parámetro defensivo para evitar inyección SQL."""
        conexion = None
        cursor = None
        try:
            conexion = ConexionBD.obtener_conexion()
            cursor = conexion.cursor(dictionary=True)

            # Paso de parámetro en tupla estricta (criterio,)
            criterio_sanitizado = criterio.strip() if criterio else ""
            cursor.callproc('sp_muestras_buscar', (criterio_sanitizado,))

            lista_resultados: List[MuestraArroz] = []
            for resultado in cursor.stored_results():
                lista_resultados.extend(MuestraArrozModel._mapear_filas(resultado.fetchall()))
            return lista_resultados

        except Exception as error_persistencia:
            raise MolinoException(f"Error en la capa DAO al buscar muestras: {error_persistencia}")

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()

    @staticmethod
    def registrar(lote: str, variedad: str, humedad_grano: float) -> int:
        """Ejecuta 'sp_muestra_registrar' (transaccional) y retorna el ID generado."""
        conexion = None
        cursor = None
        try:
            conexion = ConexionBD.obtener_conexion()
            cursor = conexion.cursor()

            # El 4to parámetro (0) es el OUT p_id_generado definido en el procedimiento
            resultado_args = cursor.callproc(
                'sp_muestra_registrar',
                (lote, variedad, humedad_grano, 0)
            )
            conexion.commit()  # mysql-connector no confirma cambios automáticamente

            id_generado = resultado_args[3]
            return id_generado

        except Exception as error_persistencia:
            if conexion is not None:
                conexion.rollback()
            # Los SIGNAL SQLSTATE '45000' del procedimiento llegan aquí como errores de negocio
            if "45000" in str(error_persistencia):
                mensaje_negocio = str(error_persistencia).split(": ", 1)[-1]
                raise ValidacionDatosError(mensaje_negocio)
            raise MolinoException(f"Error en la capa DAO al registrar la muestra: {error_persistencia}")

        finally:
            if cursor is not None:
                cursor.close()
            if conexion is not None and conexion.is_connected():
                conexion.close()
