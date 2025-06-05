class Validaciones: 
    
    
    @staticmethod
    def validar_modos (a, b):
        if a not in b: 
            return False
        else: 
            return True
        
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
    def validar_Nombre (nombre):
        if Validaciones.validar_str(nombre) and nombre.strip() != "":
            return True
        else :
            return False
