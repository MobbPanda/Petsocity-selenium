from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_modal_inicio_sesion(navegador, url_base):
    navegador.get(url_base)

    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "nav"))
    )

    # Botón del usuario en la barra de navegación (ajusta si cambia el icono)
    navegador.find_element(By.XPATH, "//nav//button[.//svg]").click()

    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//h5[contains(.,'Iniciar sesión')]"))
    )

    navegador.find_element(By.ID, "formBasicEmail").send_keys("correo@prueba.com")
    navegador.find_element(By.ID, "formBasicPassword").send_keys("ClaveSegura123")

    navegador.find_element(By.XPATH, "//div[@role='dialog']//button[normalize-space()='Iniciar sesión']").click()

    assert navegador.find_element(By.XPATH, "//div[@role='dialog']").is_displayed()
