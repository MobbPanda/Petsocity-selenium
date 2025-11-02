import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def url_base():
    # Cambia si tu app corre en otro puerto o dominio
    return os.getenv("URL_BASE", "http://localhost:3000")

@pytest.fixture(scope="session")
def navegador():
    opciones = Options()
    # Si quieres ver el navegador en acción, comenta la línea siguiente:
    opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1366,768")
    opciones.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opciones)
    yield driver
    driver.quit()

def obtener_logs(driver):
    try:
        return [e["message"] for e in driver.get_log("browser")]
    except Exception:
        return []
