import sys
from PySide6.QtWidgets import QApplication
from views.muestra_arroz_list_view import MuestraArrozListView


def principal():
    aplicacion = QApplication(sys.argv)

    # Ventana Principal directa: sin login y sin menú (requisito del escenario)
    ventana_principal = MuestraArrozListView()
    ventana_principal.show()

    sys.exit(aplicacion.exec())


if __name__ == "__main__":
    principal()
