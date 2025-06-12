import matplotlib.pyplot as plt

class Graficos: 
    
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
    def grafico_lineales(titulo, linea1, linea2, nombre_x, nombre_y, x1, y1, x2, y2): #linea 1 y linea2 son los nombres de las dos lineas
        plt.title(titulo)
        plt.xlabel(nombre_x)
        plt.ylabel(nombre_y)
        # Grafica de lineas
        plt.plot(x1,y1,color='green',linewidth=3,label=linea1)
        plt.plot(x2,y2,'o-',color='red',linewidth=3,label=linea2)



        
        