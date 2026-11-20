class MuestraArroz:
    """Clase pura de dominio: una muestra de humedad tomada a un lote de arroz en cáscara."""

    def __init__(
        self,
        id_muestra: int = None,
        lote: str = "",
        variedad: str = "",
        humedad_grano: float = 0.0,
        registrado_en=None
    ):
        self.id_muestra = id_muestra
        self.lote = lote
        self.variedad = variedad
        self.humedad_grano = humedad_grano
        self.registrado_en = registrado_en

    def __repr__(self) -> str:
        return f"<MuestraArroz id={self.id_muestra} lote='{self.lote}' humedad={self.humedad_grano}%>"
