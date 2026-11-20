# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_muestra_arroz_form.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MuestraArrozFormDialog(object):
    def setupUi(self, MuestraArrozFormDialog):
        if not MuestraArrozFormDialog.objectName():
            MuestraArrozFormDialog.setObjectName(u"MuestraArrozFormDialog")
        MuestraArrozFormDialog.resize(420, 280)
        self.verticalLayout = QVBoxLayout(MuestraArrozFormDialog)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(18, 18, 18, 18)
        self.grp_muestra = QGroupBox(MuestraArrozFormDialog)
        self.grp_muestra.setObjectName(u"grp_muestra")
        self.form_muestra = QFormLayout(self.grp_muestra)
        self.form_muestra.setObjectName(u"form_muestra")
        self.form_muestra.setVerticalSpacing(8)
        self.lbl_lote = QLabel(self.grp_muestra)
        self.lbl_lote.setObjectName(u"lbl_lote")

        self.form_muestra.setWidget(0, QFormLayout.LabelRole, self.lbl_lote)

        self.txt_lote = QLineEdit(self.grp_muestra)
        self.txt_lote.setObjectName(u"txt_lote")

        self.form_muestra.setWidget(0, QFormLayout.FieldRole, self.txt_lote)

        self.lbl_variedad = QLabel(self.grp_muestra)
        self.lbl_variedad.setObjectName(u"lbl_variedad")

        self.form_muestra.setWidget(1, QFormLayout.LabelRole, self.lbl_variedad)

        self.txt_variedad = QLineEdit(self.grp_muestra)
        self.txt_variedad.setObjectName(u"txt_variedad")

        self.form_muestra.setWidget(1, QFormLayout.FieldRole, self.txt_variedad)

        self.lbl_humedad = QLabel(self.grp_muestra)
        self.lbl_humedad.setObjectName(u"lbl_humedad")

        self.form_muestra.setWidget(2, QFormLayout.LabelRole, self.lbl_humedad)

        self.txt_humedad_grano = QLineEdit(self.grp_muestra)
        self.txt_humedad_grano.setObjectName(u"txt_humedad_grano")

        self.form_muestra.setWidget(2, QFormLayout.FieldRole, self.txt_humedad_grano)


        self.verticalLayout.addWidget(self.grp_muestra)

        self.lbl_ayuda = QLabel(MuestraArrozFormDialog)
        self.lbl_ayuda.setObjectName(u"lbl_ayuda")
        self.lbl_ayuda.setStyleSheet(u"color: #6b5b2a; font-style: italic;")
        self.lbl_ayuda.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_ayuda)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.layout_botones = QHBoxLayout()
        self.layout_botones.setObjectName(u"layout_botones")
        self.btn_guardar = QPushButton(MuestraArrozFormDialog)
        self.btn_guardar.setObjectName(u"btn_guardar")

        self.layout_botones.addWidget(self.btn_guardar)

        self.btn_cancelar = QPushButton(MuestraArrozFormDialog)
        self.btn_cancelar.setObjectName(u"btn_cancelar")

        self.layout_botones.addWidget(self.btn_cancelar)


        self.verticalLayout.addLayout(self.layout_botones)


        self.retranslateUi(MuestraArrozFormDialog)

        QMetaObject.connectSlotsByName(MuestraArrozFormDialog)
    # setupUi

    def retranslateUi(self, MuestraArrozFormDialog):
        MuestraArrozFormDialog.setWindowTitle(QCoreApplication.translate("MuestraArrozFormDialog", u"Registrar Muestra de Humedad - Arroz", None))
        self.grp_muestra.setTitle(QCoreApplication.translate("MuestraArrozFormDialog", u"Datos de la Muestra de Secado", None))
        self.lbl_lote.setText(QCoreApplication.translate("MuestraArrozFormDialog", u"Lote:", None))
        self.txt_lote.setPlaceholderText(QCoreApplication.translate("MuestraArrozFormDialog", u"Ej. LOTE-2026-045", None))
        self.lbl_variedad.setText(QCoreApplication.translate("MuestraArrozFormDialog", u"Variedad:", None))
        self.txt_variedad.setPlaceholderText(QCoreApplication.translate("MuestraArrozFormDialog", u"Ej. IR-43, Capirona, NIR-1", None))
        self.lbl_humedad.setText(QCoreApplication.translate("MuestraArrozFormDialog", u"Humedad del grano (%):", None))
        self.txt_humedad_grano.setPlaceholderText(QCoreApplication.translate("MuestraArrozFormDialog", u"Ej. 13.5", None))
        self.lbl_ayuda.setText(QCoreApplication.translate("MuestraArrozFormDialog", u"< 12.0% Grano muy seco  |  12.0%-14.0% Ideal para pilado  |  > 14.0% Riesgo de hongos", None))
        self.btn_guardar.setText(QCoreApplication.translate("MuestraArrozFormDialog", u"Guardar", None))
        self.btn_cancelar.setText(QCoreApplication.translate("MuestraArrozFormDialog", u"Cancelar", None))
    # retranslateUi

