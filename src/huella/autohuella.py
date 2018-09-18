from src.utils import get_envar, wait_between
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait



class AutoHuella(object):

    def __init__(self, url):
        self.initialize(url)

    @staticmethod
    def get_personal_data():
        return dict(
            name=get_envar('NAME'),
            nie=get_envar('NIE'),
            nation=get_envar('NATION'),
            exp_date=get_envar('EXP_DATE'),
            tel=get_envar('TEL'),
            email=get_envar('EMAIL')
        )

    def initialize(self, url):
        self.driver = webdriver.Chrome('drivers/chromedriver.exe')
        self.driver.get(url)
        self.data = self.get_personal_data()


    def provincia(self):
        options = self.driver.find_elements_by_tag_name('option')
        choice = [o for o in options if o.text.lower() == 'barcelona']
        choice[0].click()
        self.driver.execute_script("window.scrollTo(0, 100)")
        self.driver.find_element_by_link_text('Expedición de Tarjeta de Identidad de Extranjero.').click()

    def tramite(self):
        tramites = self.driver.find_elements_by_tag_name('option')
        choice = [t for t in tramites if
                  t.text == 'POLICIA-TOMA DE HUELLAS (EXPEDICIÓN DE TARJETA) Y RENOVACIÓN DE TARJETA DE LARGA DURACIÓN']
        choice[0].click()
        self.driver.execute_script("window.scrollTo(0, 100)")
        self.driver.find_element_by_id('btnAceptar').click()

    def leer(self):
        self.driver.execute_script("window.scrollTo(0, 1080)")
        self.driver.find_element_by_id('btnEntrar').click()

    def formulario(self):
        input_NIE = self.driver.find_element_by_id('txtIdCitado')
        input_NIE.send_keys(self.data['nie'])

        input_name = self.driver.find_element_by_id('txtDesCitado')
        input_name.send_keys(self.data['name'])

        country = [c for c in self.driver.find_elements_by_tag_name('option') if c.text == self.data['nation'].upper()]
        country[0].click()

        input_date = self.driver.find_element_by_id('txtFecha')
        input_date.send_keys(self.data['exp_date'])

    def check_recapcha(self):
        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name("iframe")[0])
        self.driver.find_element_by_id('recaptcha-anchor').click()
        input('Pausing for solving recaptcha, press enter to continue')

        self.driver.switch_to.default_content()
        self.driver.execute_script("window.scrollTo(0, 1080)")
        self.driver.find_element_by_id('btnEnviar').click()

    def solicitar(self):
        wait_between(2,3)
        self.driver.find_element_by_id('btnEnviar').click()

    def oficina(self):
        oficina = self.driver.find_elements_by_tag_name('option')
        choose_office = input('Office No. ? from {}'.format([o.text for o in oficina]))
        oficina[int(choose_office)].click()
        self.driver.execute_script("window.scrollTo(0, 100)")
        self.driver.find_element_by_id('btnSiguiente').click()

    def datos(self):
        input_cell = self.driver.find_element_by_id('txtTelefonoCitado')
        input_cell.send_keys(self.data['tel'])

        input_email = self.driver.find_element_by_id('emailUNO')
        input_email.send_keys(self.data['email'])

        input_email2 = self.driver.find_element_by_id('emailDOS')
        input_email2.send_keys(self.data['email'])

        self.driver.find_element_by_id('btnSiguiente').click()

    def hay_cita(self):
        info = self.driver.find_element_by_class_name('mf-msg__info').text.split('\n')[0]
        if info == 'NO HAY SUFICIENTES CITAS DISPONIBLES':
            print(info)
            return False
        else:
            return True

    def cerrar(self):
        self.driver.close()