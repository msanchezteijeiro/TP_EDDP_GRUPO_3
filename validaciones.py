#VALIDACIONES GENERALES PARA VALIDAR DATOS DE ENTRADA

#Si aca importamos otra clase, se rompe todo.
#Porque al importar otra clase, se importa todo el modulo, y si el modulo tiene un import de este modulo, se rompe la recursividad.

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


    