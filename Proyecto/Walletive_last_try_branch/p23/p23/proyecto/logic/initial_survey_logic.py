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
        tiene_deudas = self.respuestas[4] # Ya es "Sí" o "No"
        total_deuda = self._to_float(self.respuestas[5]) if tiene_deudas == "Sí" else 0.0
        cuota_mensual = self._to_float(self.respuestas[6]) if tiene_deudas == "Sí" else 0.0
        tiene_meta = self.respuestas[7] # Ya es "Sí" o "No"
        meta_ahorro = self._to_float(self.respuestas[8]) if tiene_meta == "Sí" else 0.0
        meses_meta = int(self.respuestas[9]) if tiene_meta == "Sí" else 0

        # Cálculo de ahorro potencial (esto es solo informativo, no se guarda directamente en DB)
        ahorro_estimado = ingreso - (fijos + variables + cuota_mensual)

        # Llamada a la capa de persistencia
        # La función guardar_datos_encuesta en DatabaseManager ahora maneja la inserción
        # de los movimientos iniciales y la meta de ahorro.
        self.db.guardar_datos_encuesta(nombre, [
            ingreso, fijos, variables,
            tiene_deudas, total_deuda, cuota_mensual,
            tiene_meta, meta_ahorro, meses_meta
        ])

        return ahorro_estimado

    @staticmethod
    def _to_float(valor):
        """Intenta convertir valor a float, devuelve 0.0 en caso de error."""
        try:
            # Asegurarse de que el valor sea una cadena antes de reemplazar
            if isinstance(valor, (int, float)):
                return float(valor)
            return float(str(valor).replace(",",""))
        except (ValueError, TypeError):
            return 0.0

