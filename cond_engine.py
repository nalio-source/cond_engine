NOME_PROGRAMMA      = "COND ENGINE"
CREATORE_PROGRAMMA  = "NALIo"
DATA_CREAZIONE      = "26/05/2023"
VERSIONE_ATTUALE    = "0.0.0.9"
ULTIMO_UPDATE       = "29/06/2023"

MODIFICHE           = "Risolto bug riempi; aggiunto +1 nel ridimensiona della visuale"
COSE_DA_FARE        = "Metti che puoi essere anche in una mappa più piccola della visuale"


from sys import stdout
from os import system
from time import sleep 


NERO = '\033[30m'
BIANCO = '\033[00m'
ROSSO = '\033[31m'
ROSA = '\033[91m'
OCRA = '\033[33m'
GIALLO = '\033[93m'
VERDE = '\033[92m'
VERDE_SCURO = '\033[32m'
ACQUA = '\033[96m'
CELESTE = '\033[36m'
AZZURRO = '\033[94m'
BLU = '\033[34m'
FUCSIA = '\033[95m'
VIOLA = '\033[35m'
TEXTURE = {
    "blocco": "█",
    "semi_ombra": "▓",
    "ombra": "▒",
    "trasparente": "░",
    "spazio": " ",
    "linea_orizzontale": "─",
    "linea_verticale": "│",
    "angolo_alto_sx": "┌",
    "angolo_alto_dx": "┐",
    "angolo_basso_sx": "└",
    "angolo_basso_dx": "┘",
}

MARGINE_BORDO = [3,5]  # margine extra aggiunto alla distanza della visuale dai bordi


def write(stringa):
    stdout.write(str(stringa)+"\n")


def elimina_linee(n_linee=1): 
    for k in range(n_linee): 
        stdout.write('\033[F')


def ridimensiona_finestra(x, y, dimensione=11):
    """In x metti quanti caratteri vedere orizzontalmente (ricorda di 
    moltiplicarlo sempre per 2 se stai usando una grafica), invece in
    y metti quanti caratteri vedere verticalmente
    """
    system(f"mode con cols={x} lines={y}")


def cambia_nome_finestra(nome):
    system(f"title {nome}")


class Grafica():
    """Classe principale del cond engine, con la quale si può istanziare
    una grafica 2D a griglia. \n
    Ricorda di mettere sempre <colorata = False> se non si vogliono i colori.\n
    Se len(sfondo) <= 5 ---> colorata diventa False in automatico\n
    Al contrario, se si vogliono i colori, aggiungili al parametro sfondo se deve essere cambiato\n
    La grafica non colorata ovviamente richiede meno potere computazionale (gli fps raddoppiano)\n
    """
    def __init__(self, dimensione, sfondo=BIANCO+TEXTURE["trasparente"]*2, colorata=True):
        self.dimensione = dimensione
        self.len_pixel = len(sfondo)  # quanto è grande la stringa di ogni pixel (ad esempio i colori aggiungono 5 alla lunghezza len('\033[00mCIAO') = 9)
        self.colorata = colorata   # booleano
        if self.len_pixel <= 5: self.colorata = False
        self.sfondo = sfondo
        if self.colorata: 
            self.colore_sfondo = self.sfondo[:5]
            self.len_pixel_no_colore = self.len_pixel-5  # la parte del colore (ad esempio \033[00m) viene esclusa
        else: self.len_pixel_no_colore = self.len_pixel
        self.grafica = ""
    
    def genera(self):   # è più veloce di un join
        linea = ""
        for x in range(self.dimensione[0]):
            linea += self.sfondo
        self.grafica = ""
        for k in range(self.dimensione[1]):
            self.grafica += linea

    def riempi(self, texture):
        self.sfondo = texture
        self.genera()
    
    def controllo_pixel(self, coordinate):
        if coordinate[0] < self.dimensione[0] and coordinate[1] < self.dimensione[1] and coordinate[0] >= 0 and coordinate[1] >= 0:
            obiettivo = self.len_pixel*(coordinate[0]+(coordinate[1]*self.dimensione[0]))
            return self.grafica[obiettivo:obiettivo+self.len_pixel]
        else: return self.sfondo
    
    def aggiungi_pixel(self, coordinate, texture_pixel):
        coord = (self.dimensione[0]*coordinate[1]+coordinate[0]+1)*self.len_pixel
        self.grafica = self.grafica[:coord-self.len_pixel] + texture_pixel + self.grafica[coord:]
    
    def aggiungi_linea(self, coordinata_sx, coordinata_dx, texture_linea):
        """Ti permette di aggiungere una linea di texture orizzontale da una coordinata iniziale sx a una coordinata finale dx"""
        coord_sx = (self.dimensione[0]*coordinata_sx[1]+coordinata_sx[0]+1)*self.len_pixel
        coord_dx = (self.dimensione[0]*coordinata_dx[1]+coordinata_dx[0]+1)*self.len_pixel
        self.grafica = self.grafica[:coord_sx-self.len_pixel] + texture_linea + self.grafica[coord_dx:]
    
    def rimuovi_pixel(self, coordinate):
        coord = (self.dimensione[0]*coordinate[1]+coordinate[0]+1)*self.len_pixel
        self.grafica = self.grafica[:coord-self.len_pixel] + self.sfondo + self.grafica[coord:]
    
    def aggiungi_scritta(self, coordinate, scritta):
        if len(scritta)%2 == 1:
            scritta += " "
        for k in range(int(len(scritta)/2)):
            coord = (self.dimensione[0]*(coordinate[1])+coordinate[0]+k)*self.len_pixel
            self.grafica = self.grafica[:coord-self.len_pixel] + "\033[00m" + scritta[k*2] + scritta[k*2+1] + self.grafica[coord:]  

    def mostra(self):
        cont_gr = 0
        for k in range(self.dimensione[1]):
            write(self.grafica[cont_gr: cont_gr + (self.dimensione[0]*self.len_pixel): 1])
            cont_gr = cont_gr + (self.dimensione[0]*self.len_pixel)


class Visuale():
    """Con questa classe si può generare e gestire la visuale del player"""
    def __init__(self, dimensione, grafica, distanza = [0,0]):
        self.dimensione = dimensione
        self.distanza = distanza
        self.grafica = grafica
        ridimensiona_finestra((self.dimensione[0]+self.distanza[0])*(self.grafica.len_pixel_no_colore)*2+MARGINE_BORDO[0]+1, (self.dimensione[1]+self.distanza[1])*2+MARGINE_BORDO[1])

    def mostra(self, coordinata, colore_esterno=BIANCO):
        if not self.grafica.colorata: colore = "" # se la grafica è in bianco e nero, non vengono aggiunti colori
        else: colore = colore_esterno
        visuale = ""
        salt_x = coordinata[0]-self.dimensione[0]
        salt_y = coordinata[1]-self.dimensione[1]
        linea_dritta = ""
        for k in range((((self.dimensione[0]*2)+1)*self.grafica.len_pixel_no_colore)):
            linea_dritta += f"{colore}{TEXTURE['linea_orizzontale']}"
        elimina_linee(((self.dimensione[1]+self.distanza[1])*2)+MARGINE_BORDO[1])
        for k in range(self.distanza[1]):
            write("")
        linea_distanza = ""
        texture_spazio_bilanciata = TEXTURE['spazio']*self.grafica.len_pixel_no_colore   # è basato sulla len_pixel della grafica
        for k in range(self.distanza[0]):
            linea_distanza += f"{colore}{texture_spazio_bilanciata}"
        write(f"{linea_distanza}{colore}{TEXTURE['angolo_alto_sx']}"+linea_dritta+f"{colore}{TEXTURE['angolo_alto_dx']}")
        for k in range((self.dimensione[1]*2)+1):
            visuale = ""
            for j in range((self.dimensione[0]*2)+1):
                cod_visuale = (((salt_x+j)+(self.grafica.dimensione[0]*(salt_y+k)))*self.grafica.len_pixel)
                if cod_visuale >= 0 and cod_visuale < self.grafica.dimensione[0]*self.grafica.dimensione[1]*self.grafica.len_pixel and salt_x+j >= 0 and salt_y+k >= 0 and salt_x+j < self.grafica.dimensione[0] and salt_y+k < self.grafica.dimensione[1]:
                    visuale += self.grafica.grafica[cod_visuale:cod_visuale+self.grafica.len_pixel]
            for j in range(int(((((self.dimensione[0]*2)+1)*self.grafica.len_pixel)-len(visuale))/self.grafica.len_pixel)):    # questa linea crea uno spazio se il player è vicino al bordo della mappa
                if coordinata[0] <= int(self.grafica.dimensione[0]/2):
                    visuale = f"{colore}{texture_spazio_bilanciata}{visuale}"
                else:
                    visuale += f"{colore}{texture_spazio_bilanciata}"
            write(f"{linea_distanza}{colore}{TEXTURE['linea_verticale']}{visuale}{colore}{TEXTURE['linea_verticale']}")
        write(f"{linea_distanza}{colore}{TEXTURE['angolo_basso_sx']}{linea_dritta}{colore}{TEXTURE['angolo_basso_dx']}")


if __name__ == "__main__" or True:   # non metto __name__ == "cond_engine" perché se è il nome del file cambia è un casino
    system("cls")
    cambia_nome_finestra("COND ENGINE")
    ridimensiona_finestra(52, 13)
    print(f"{BIANCO}MADE WITH")
    benvenuto = Grafica([25,9], sfondo="  ")
    benvenuto.grafica = "                                                    ██████  ██████  ██    ██  ████                    ██      ██  ██  ████  ██  ██  ██                  ██████  ██████  ██  ████  ████    ██                                                                ██████  ██    ██  ██████  ██  ██    ██  ██████    ████    ████  ██  ██      ██  ████  ██  ████      ██      ██  ████  ██  ██  ██  ██  ████  ██        ██████  ██    ██  ██████  ██  ██    ██  ██████  "
    benvenuto.mostra()
    print(f"\nMADE BY {CREATORE_PROGRAMMA} - - - - - - - - - - VERSION {VERSIONE_ATTUALE}")
    sleep(2)
