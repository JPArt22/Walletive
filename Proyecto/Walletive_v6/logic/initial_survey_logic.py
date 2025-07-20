# logic/initial_survey_logic.py

from persistence.database_manager import DatabaseManager


class InitialSurveyLogic:
    """
    Procesa, valida y persiste los resultados de la encuesta inicial.
    """

    def __init__(self, respuestas: list):
        self.respuestas = respuestas
        self.db = DatabaseManager()

    def procesar_y_guardar(self):
        """
        Convierte las respuestas, calcula valores derivados y guarda
        todos los datos en la base de datos mediante DatabaseManager.
        """
        nombre = self.respuestas[0]
        ingreso = self._to_float(self.respuestas[1])
        fijos = self._to_float(self.respuestas[2])
        variables = self._to_float(self.respuestas[3])
        tiene_deudas = self.respuestas[4] == "Sí"
        total_deuda = self._to_float(self.respuestas[5]) if tiene_deudas else 0.0
        cuota_mensual = self._to_float(self.respuestas[6]) if tiene_deudas else 0.0
        tiene_meta = self.respuestas[7] == "Sí"
        descripcion_meta = self.respuestas[8] if tiene_meta else ""
        meta_ahorro = self._to_float(self.respuestas[9]) if tiene_meta else 0.0
        meses_meta = int(self.respuestas[10]) if tiene_meta else 0

        # Cálculo de ahorro potencial
        ahorro_estimado = ingreso - (fijos + variables + cuota_mensual)

        # Prepara diccionario de datos
        usuario_data = {
            "nombre": nombre,
            "ingreso": ingreso,
            "gastos_fijos": fijos,
            "gastos_variables": variables,
            "tiene_deudas": tiene_deudas,
            "total_deuda": total_deuda,
            "cuota_mensual": cuota_mensual,
            "tiene_meta": tiene_meta,
            "meta_ahorro": meta_ahorro,
            "meses_meta": meses_meta,
            "ahorro_estimado": ahorro_estimado
        }

        # --- CORRECCIÓN ---
        # 1. Guardar primero todas las respuestas de la encuesta
        self.db.guardar_datos_encuesta(nombre, [
            ingreso, fijos, variables,
            "Sí" if tiene_deudas else "No", total_deuda, cuota_mensual,
            "Sí" if tiene_meta else "No", descripcion_meta, meta_ahorro, meses_meta
        ])

        # 2. Si el usuario indicó que tiene una meta, la creamos en la BD
        if tiene_meta and descripcion_meta.strip() and meta_ahorro > 0 and meses_meta > 0:
            print(f"🌱 Creando meta inicial: '{descripcion_meta}' por ${meta_ahorro} en {meses_meta} meses.")
            self.db.crear_meta(
                descripcion=descripcion_meta,
                monto_objetivo=meta_ahorro,
                meses=meses_meta
            )
        # --------------------

        return ahorro_estimado

    @staticmethod
    def _to_float(valor):
        """Intenta convertir valor a float, devuelve 0.0 en caso de error."""
        try:
            return float(valor)
        except (ValueError, TypeError):
            return 0.0
