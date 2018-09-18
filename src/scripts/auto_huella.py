from src.huella.autohuella import AutoHuella
import ctypes
from src.utils import wait_between

url = 'https://sede.administracionespublicas.gob.es/icpplus/'



def main(url):
    ah = AutoHuella(url)
    ah.provincia()
    ah.tramite()
    ah.leer()
    ah.formulario()
    ah.check_recapcha()
    ah.solicitar()
    ah.oficina()
    ah.datos()
    if ah.hay_cita():
        ctypes.windll.user32.MessageBoxW(0, "CITA!!!!!", "CITA!!!!!", 1)
    else:
        ah.cerrar()
        wait_between(5,10)
        main(url)


if __name__ == '__main__':
    main(url)
