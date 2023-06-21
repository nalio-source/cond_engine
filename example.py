# Esempio molto primitivo di una possibile applicazione del cond_engine

from os import system
from cond_engine import *


DIMENSIONE_GRAFICA = [100, 100]
DIMENSIONE_VISUALE = [28, 13]
BORDI_VUOTI_VISUALE = [10,4]

mondo = Grafica(DIMENSIONE_GRAFICA)    
mondo.genera()         # genera la grafica (sempre necessario all'inizio)
visuale = Visuale(DIMENSIONE_VISUALE, mondo, BORDI_VUOTI_VISUALE)
posizione = [0,0]
system("cls") # calorosamente consigliato


def main():
    while True:
        # gestione del player
        posizione[0] += 1
        if posizione[0] >= DIMENSIONE_GRAFICA[0]-1:
            posizione[0] = 0
        
        # gestione della grafica
        mondo.genera()   # svota la visuale da tutte le entità  (un'alternativa più veloce potrebbe essere questa: mondo.grafica = grafica_default)
        mondo.aggiungi_pixel(posizione, ROSSO+TEXTURE["ombra"]*2)         # aggiunge il pixel del player
        mondo.aggiungi_linea([10, 10], [13, 10], (BIANCO+TEXTURE["blocco"]*2)*4)         # aggiunge dei pixel bianchi
        visuale.mostra(posizione, colore_esterno=ROSSO)


if __name__ == "__main__":
    main()
