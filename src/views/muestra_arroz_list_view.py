from PySide6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView, QDialog
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt

from views.frm_muestra_arroz_list_ui import Ui_Form
from views.muestra_arroz_form_dialog import MuestraArrozFormDialog
from controllers.muestra_arroz_controller import MuestraArrozController
from exceptions.molino_exceptions import MolinoException

# Colores corporativos para la columna "Estado de Humedad" (semáforo de riesgo)
COLOR_MUY_SECO = QColor("#fde2b0")     # ámbar: riesgo de quiebre
COLOR_IDEAL = QColor("#d7f0d1")        # verde: humedad ideal
COLOR_RIESGO_HONGOS = QColor("#f7c9c3")  # rojo claro: riesgo de hongos


class MuestraArrozListView(QWidget, Ui_Form):
    """Ventana Principal (Listado y Búsqueda) del módulo de Control de Humedad de Arroz."""

    def __init__(self, padre=None):
        super().__init__(padre)
        self.setupUi(self)

        self._controlador = MuestraArrozController()

        self._configurar_cabeceras_tabla()
        self.txt_buscar.setClearButtonEnabled(True)

        self.btn_buscar.clicked.connect(self._ejecutar_busqueda)
        self.txt_buscar.returnPressed.connect(self._ejecutar_busqueda)
        self.txt_buscar.textChanged.connect(self._al_cambiar_texto_busqueda)

        self.btn_nuevo.clicked.connect(self._al_hacer_clic_nuevo)

        # Carga inicial de datos desde MySQL al abrir la ventana
        self._cargar_grilla()

    def _configurar_cabeceras_tabla(self):
        cabecera = self.tbl_muestras.horizontalHeader()
        cabecera.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        cabecera.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        cabecera.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        cabecera.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        cabecera.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    def _cargar_grilla(self):
        """Solicita el listado completo al controlador y renderiza la tabla."""
        try:
            lista_muestras = self._controlador.obtener_todas()
            self._renderizar_datos(lista_muestras)
        except MolinoException as error:
            QMessageBox.critical(self, "Error de Conexión", str(error))

    def _ejecutar_busqueda(self):
        """Búsqueda en tiempo real por lote o variedad."""
        criterio = self.txt_buscar.text()
        try:
            lista_filtrada = self._controlador.buscar_muestras(criterio)
            self._renderizar_datos(lista_filtrada)
        except MolinoException as error:
            QMessageBox.critical(self, "Error de Búsqueda", str(error))

    def _al_cambiar_texto_busqueda(self, nuevo_texto: str):
        """Si la caja se vacía (por borrar todo o presionar la 'X'), restaura el listado."""
        if not nuevo_texto.strip():
            self._cargar_grilla()

    def _renderizar_datos(self, coleccion_muestras):
        self.tbl_muestras.setRowCount(0)

        for fila_idx, muestra in enumerate(coleccion_muestras):
            self.tbl_muestras.insertRow(fila_idx)

            mensaje_alerta = self._controlador.evaluar_alerta_humedad(muestra.humedad_grano)
            color_fila = self._color_segun_alerta(mensaje_alerta)

            item_lote = QTableWidgetItem(muestra.lote)
            item_lote.setData(99, muestra.id_muestra)
            item_lote.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_variedad = QTableWidgetItem(muestra.variedad)

            item_humedad = QTableWidgetItem(f"{muestra.humedad_grano:.2f}")
            item_humedad.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            item_estado = QTableWidgetItem(mensaje_alerta)
            item_estado.setBackground(QBrush(color_fila))

            fecha_str = str(muestra.registrado_en) if muestra.registrado_en else "N/A"
            item_fecha = QTableWidgetItem(fecha_str)
            item_fecha.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            for item in (item_lote, item_variedad, item_humedad, item_estado, item_fecha):
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            self.tbl_muestras.setItem(fila_idx, 0, item_lote)
            self.tbl_muestras.setItem(fila_idx, 1, item_variedad)
            self.tbl_muestras.setItem(fila_idx, 2, item_humedad)
            self.tbl_muestras.setItem(fila_idx, 3, item_estado)
            self.tbl_muestras.setItem(fila_idx, 4, item_fecha)

        if hasattr(self, 'label_2'):
            self.label_2.setText(f"Se muestran los últimos ({len(coleccion_muestras)}) registros")

    @staticmethod
    def _color_segun_alerta(mensaje_alerta: str) -> QColor:
        if "QUIEBRE" in mensaje_alerta:
            return COLOR_MUY_SECO
        if "HONGOS" in mensaje_alerta:
            return COLOR_RIESGO_HONGOS
        return COLOR_IDEAL

    def _al_hacer_clic_nuevo(self):
        """Abre el modal de Registro; si se guarda, refresca la grilla al instante."""
        modal_registro = MuestraArrozFormDialog(parent=self)
        if modal_registro.exec() == QDialog.DialogCode.Accepted:
            self._cargar_grilla()
