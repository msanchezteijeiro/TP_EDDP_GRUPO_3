import matplotlib.pyplot as plt

class Grafico: 
    
    @staticmethod
    def grafico_barras(titulo, nombre_x, nombre_y, lista_x, lista_y):
        plt.title(label= titulo, fontsize=20, color='blue')
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        plt.bar(lista_x, lista_y,color='green',width=0.5)

    @staticmethod
    def grafico_linea(valores):
        plt.plot(valores)


    @staticmethod
    def grafico_torta(titulo, secciones, cantidades):
        plt.pie(cantidades,labels=secciones, autopct='%1.2f%%')
        plt.title(label=titulo, loc='center', color='blue')
    
    @staticmethod 
    def grafico_lineal(titulo, nombre_x, nombre_y, x1, y1): #linea 1 y linea2 son los nombres de las dos lineas
        plt.title(titulo)
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        # Grafica de lineas
        plt.plot(x1,y1,color='green',linewidth=3)


#Grafico Tiempo vs Distancia Recorrida (FALTA PONER LOS DATOS DE TIEMPO Y DISTANCIA)
Grafico.grafico_lineal("Tiempo vs Distancia", "Tiempo [min]", "Distancia [km]", )

#Grafico Costo por Distancia Recorrida (FALTA PONER LOS DATOS DE COSTO Y DISTANCIA)
Grafico.grafico_lineal("Costo vs Distancia", "Costo [$]", "Distancia [km]", )




        
        