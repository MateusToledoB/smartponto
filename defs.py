from defs_TIP import * 
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
from selenium import webdriver
import sys
import os

if getattr(sys, 'frozen', False):
    # Quando rodando no .exe gerado pelo cx_Freeze
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Quando rodando direto no Python
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def iniciar_driver_edge(caminho_driver):
    options = Options()
    service = EdgeService(executable_path=caminho_driver)
    try:
        driver = webdriver.Edge(service=service, options=options)
        return driver
    except Exception as e:
        print(f"Ocorreu um erro ao iniciar o driver: {e}")
        return None

def subir_folhas(user, senha, driver_option, pasta):
    match driver_option:
        case "137":
            caminho_driver = os.path.join(BASE_DIR, "drivers", "edgedriver_win64137", "msedgedriver.exe")
        case "138":
            caminho_driver = os.path.join(BASE_DIR, "drivers", "edgedriver_win64138", "msedgedriver.exe")
        case "139":
            caminho_driver = os.path.join(BASE_DIR, "drivers", "edgedriver_win64139", "msedgedriver.exe")
        case "140":
            caminho_driver = os.path.join(BASE_DIR, "drivers", "edgedriver_win64140", "msedgedriver.exe")
        case _:
            print("Opção de driver inválida.")
            return
    driver = None
    
    try:
        driver = iniciar_driver_edge(caminho_driver)
        if driver is None:
            print("Falha ao iniciar o driver. Abortando.")
            return

        time.sleep(7)
        usuario(driver, user, senha)
        for nome in os.listdir(pasta):

            caminho_completo = os.path.join(pasta, nome)
            partes = nome.split('-')
            cpf = str(partes[0]).strip().zfill(11)
            competencia_1 = str(partes[1])
            competencia_partes = competencia_1.split('.')
            competencia_mes = str(competencia_partes[0]).strip()
            competencia_mes = f"{int(competencia_mes):02}"
            competencia = f'{competencia_mes}/2025'
            comp_portal = f'2025{competencia_mes}'

            try:
                vai_card(driver, cpf)
                time.sleep(2)
                click_webelement(driver, "//*[@ID='ext-element-7']", 0)
                click(driver, "//*[text()='5.40 - FOLHA PONTO']")
                try:
                    acessar_relatorio(driver,"/html/body/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/iframe")
                    time.sleep(8)
                    escrever(driver, "//*[@ID='textfield-1023-inputEl']", comp_portal)
                    time.sleep(2)
                    xpath = "//*[text()='ASSINADO']"
                    element = driver.find_element(By.XPATH,xpath)
                    close_tabs_except_first(driver)
                    time.sleep(2)
                except:
                    time.sleep(1.5)
                    foca_aba(driver, "G360")
                    time.sleep(2)
                    click_webelement(driver, "//*[@ID='ext-element-7']", 0)
                    time.sleep(1)
                    click(driver, "//*[text()='5.80 - INCLUIR DOCUMENTO']")
                    time.sleep(4)
                    acessar_relatorio(driver,"/html/body/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div[2]/div[1]/div/iframe")
                    time.sleep(2)
                    click(driver, "//*[@ID='cbbGruposDocumentos-trigger-picker']")
                    time.sleep(1)
                    click(driver, "//*[text()='FOLHA DE PONTO']")
                    time.sleep(2)
                    click(driver, "//*[@ID='cbbTiposDocumentos-trigger-picker']")
                    time.sleep(1)
                    click(driver, "//*[text()='FOLHA DE PONTO MANUAL COM COMPETENCIA']")
                    time.sleep(2)
                    input_element = driver.find_element(By.XPATH, "//*[@ID='dtCompetencia2627-inputEl']")
                    time.sleep(2)
                    driver.execute_script(f"arguments[0].value = '{competencia}';", input_element)
                    time.sleep(1)
                    click(driver, "//*[@id='dtCompetencia2627-inputEl']")
                    time.sleep(1)
                    click(driver, "//*[@id='dtCompetencia2627-inputEl']")
                    time.sleep(2)
                    input_element = driver.find_element(By.XPATH, "//*[@id='fupNovoDocumento-button-fileInputEl']")
                    input_element.send_keys(caminho_completo)
                    time.sleep(2)
                    click(driver, "//*[@id='btnSalvar-btnEl']")
                    time.sleep(15)
                    esperar_elemento(driver, "//*[text()='Carregando...']", 200)
                    close_tabs_except_first(driver)
                    time.sleep(3)
            except Exception as e:
                print(f"Erro na iteração do arquivo '{nome}': {e}")
                time.sleep(1.5)
                close_tabs_except_first(driver)
                time.sleep(1)
    except Exception as e:
        print(f"Erro geral na função subir_folhas: {e}")
    finally:
        if driver:
            driver.quit()
