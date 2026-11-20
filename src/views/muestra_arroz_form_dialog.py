from PySide6.QtWidgets import QDialog, QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression

from views.frm_muestra_arroz_form_ui import Ui_MuestraArrozFormDialog
from controllers.muestra_arroz_controller import MuestraArrozController
from exceptions.molino_exceptions import ValidacionDatosError, MolinoException


class MuestraArrozFormDialog(QDialog, Ui_MuestraArrozFormDialog):
    """Ventana modal de Registro: captura una nueva muestra de humedad y la guarda en MySQL."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self._controlador = MuestraArrozController()

        self._configurar_validadores_interfaz()

        self.btn_guardar.clicked.connect(self._al_guardar)
        self.btn_cancelar.clicked.connect(self.reject)

    def _configurar_validadores_interfaz(self):
        """Restringe la caja de humedad a números decimales (ej. 13.5)."""
        self.txt_lote.setMaxLength(20)
        self.txt_variedad.setMaxLength(60)

        regex_decimal = QRegularExpression(r"^\d{0,3}([.,]\d{0,2})?$")
        self.txt_humedad_grano.setValidator(QRegularExpressionValidator(regex_decimal, self))

    def _al_guardar(self):
        """Envía los datos capturados al Controlador y muestra el resultado en pantalla."""
        lote = self.txt_lote.text()
        variedad = self.txt_variedad.text()
        humedad_texto = self.txt_humedad_grano.text()

        try:
            id_generado, mensaje_alerta = self._controlador.registrar_muestra(
                lote, variedad, humedad_texto
            )
            QMessageBox.information(
                self,
                "Registro Confirmado",
                f"Muestra registrada exitosamente con ID: {id_generado}\n\n"
                f"Resultado del análisis de humedad:\n{mensaje_alerta}"
            )
            self.accept()

        except ValidacionDatosError as advertencia:
            # Respuesta interactiva ante errores de entrada del operador
            QMessageBox.warning(self, "Validación de Formulario", str(advertencia))

        except MolinoException as error_bd:
            # Respuesta crítica ante fallas en base de datos o transacciones
            QMessageBox.critical(self, "Falla Transaccional", str(error_bd))
