# Programacion III N612, Carlos Ferrer CI 28.326.446 y Diego Sanchez CI 29.761.545 

# Instalar librerias correspondientes:
# pip install pycoingecko
# pip install pyqt5
# pip installl pyqt5-tools
# pip install pyinstaller


import PyQt5
from os import name
import sys,re
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, qAlpha
from PyQt5.QtWidgets import QMainWindow, QApplication,QLineEdit,QDialog,QMessageBox
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import json

class principal (QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("diseño.ui",self)

        #Add Imagen
        self.imagelabel.setPixmap(QtGui.QPixmap("cryptoviewerlogo.png"))

        # Cuadro para eliminar texto
        self.dato_crypto.setClearButtonEnabled(True)
        self.dato_moneda.setClearButtonEnabled(True)

        # Codigo para realizar el evento de las validaciones
        self.dato_crypto.textChanged.connect(self.validar_crypto)
        self.dato_moneda.textChanged.connect(self.validar_moneda)

        # Boton para crear el evento que muestra los resultados
        self.botonBuscar.pressed.connect(self.showResults)
        

     # Funcion para validar datos de moneda
    def validar_crypto(self):
        dato_crypto = self.dato_crypto.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$',dato_crypto, re.I)
        if dato_crypto == "":
            self.dato_crypto.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.dato_crypto.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.dato_crypto.setStyleSheet("border: 1px solid green;")
            return True

    # Funcion para validar datos de moneda
    def validar_moneda(self):
        dato_moneda = self.dato_moneda.text()
        validar = re.match('^[a-z\sáéíóúàèìòùäëïöüñ]+$',dato_moneda, re.I)
        if dato_moneda == "":
            self.dato_moneda.setStyleSheet("border: 1px solid yellow;")
            return False
        elif not validar:
            self.dato_moneda.setStyleSheet("border: 1px solid red;")
            return False
        else:
            self.dato_moneda.setStyleSheet("border: 1px solid green;")
            return True    

    # Funcion que muestra los resultados en los botones pertinentes
    def showResults(self):
        
        # Ejecutamos si los datos estan validados
        if self.validar_crypto() and self.validar_moneda():

            # Guardamos los datos en variables
            self.crypto = str()
            self.moneda = str()
            
            self.crypto = str (self.dato_crypto.text())
            self.moneda = str (self.dato_moneda.text())
            
            # Scrapping de los datos a la API
            self.precio = cg.get_price(ids=self.crypto, vs_currencies=self.moneda, include_market_cap='true', include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')

            # Parsea el diccionario a cadena string, guardandolo en la variable precio
            self.resultado = json.dumps(self.precio)

            # Eliminar las llaves, y hacer las separaciones correspondientes
            self.separador = ","
            self.max_separaciones = 4
            self.resultado2 = self.resultado.split(self.separador, self.max_separaciones)

            # Buscas las llaves en la cadena string (resultado)
            self.buscar = "{"
            self.buscar_2 = "}"
            self.change = ""

            # Eliminar las llaves
            self.resultado_2 = self.resultado.replace(self.buscar,self.change)
            self.resultado_3 = self.resultado_2.replace(self.buscar_2,self.change)

            # Volvemos a separar los elementos
            self.separador = ","
            self.max_separaciones = 5
            self.resultado_4 = self.resultado_3.split(self.separador, self.max_separaciones)

            # Agregamos los valores a variables distintas
            self.cryptodata1 = self.resultado_4[0]
            self.cryptodata2 = self.resultado_4[1]
            self.cryptodata3 = self.resultado_4[2]
            self.cryptodata4 = self.resultado_4[3]
    
            # Enviamos los datos a las cajas de texto que mostraran los resultados
            self.dato_precio.setText(str(self.cryptodata1))
            self.dato_volumen.setText(str(self.cryptodata2))
            self.dato_24h.setText(str(self.cryptodata3))
            self.dato_marketvet.setText(str(self.cryptodata4))
        
        # Mostramos mensaje de que 
        else:
            QMessageBox.warning(self,"Datos Incorrectos","Digite los datos correctamente",QMessageBox.Discard)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = principal()
    GUI.show()
    sys.exit(app.exec_())

