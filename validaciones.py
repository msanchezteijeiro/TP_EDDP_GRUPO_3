#VALIDACIONES GENERALES PARA VALIDAR DATOS DE ENTRADA

class Validaciones: 

    @staticmethod
    def validar_float (a): 
        if not isinstance (a, float): 
            return False
        else :
            return True
        
           
    @staticmethod
    def validar_int (a): 
        if not isinstance (a, int): 
            return False
        else :
            return True

    @staticmethod
    def validar_str (a): 
        if not isinstance (a, str): 
            return False
        else :
            return True
    
    @staticmethod
    def validar_nombre (nombre):
        if Validaciones.validar_str(nombre) and nombre.strip() != "": #nombre.strip() obtiene la cadena sin espacios y comparamos con "" para asegurarnos q no sea vacia
            return True
        else :
            return False
        
    @staticmethod
    def validar_tipo_restriccion(tipo_restriccion):
        tipos_restriccion_validas = ["peso_max", "velocidad_max", "prob_mal_tiempo", "tipo", "", None]
        if tipo_restriccion in tipos_restriccion_validas:
            return True

        elif tipo_restriccion is None and not Validaciones.validar_str(tipo_restriccion):
            raise TypeError("La restriccion debe ser una cadena de texto o None.")

        if tipo_restriccion not in tipos_restriccion_validas:
            raise ValueError(f"Restriccion no reconocida: {tipo_restriccion}")


    @staticmethod
    def validar_tipo_restriccion(tipo_restriccion):
        restricciones_validas = ["peso_max", "velocidad_max", "prob_mal_tiempo", "tipo", "", None]

        if tipo_restriccion is None:
            return True

        if Validaciones.validar_str(tipo_restriccion):
            return tipo_restriccion in restricciones_validas

        return False

    @staticmethod
    def validar_valor_restriccion(valor_restriccion):
        valores_restriccion_validos = ["fluvial", "maritimo", None]

        if valor_restriccion in valores_restriccion_validos:
            return True

        try:
            float(valor_restriccion)  # sirve para ambos: int y float
            return True
        except ValueError:
            return False



    