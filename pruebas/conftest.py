import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="session")
def url_base():
    # Cambiar si la pagina corre en otro puerto o dominio
    return os.getenv("URL_BASE", "http://localhost:3000")

@pytest.fixture(scope="session")
def navegador():
    opciones = Options()
    # Si quieres ver el navegador, comenta la siguiente línea
    # opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1366,768")
    opciones.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    # Forma correcta de inicializar el driver
    from selenium.webdriver.chrome.service import Service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opciones)

    yield driver
    driver.quit()

@pytest.fixture
def obtener_logs():
    def _get(driver):
        try:
            return [e["message"] for e in driver.get_log("browser")]
        except Exception:
            return []
    return _get