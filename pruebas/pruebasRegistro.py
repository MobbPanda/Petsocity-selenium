import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from configuracion import obtener_logs

def test_registro_exitoso(navegador, url_base):
    navegador.get(f"{url_base}/registrarUsuario")

    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Registro de usuario')]"))
    )

    navegador.find_element(By.ID, "nombreCompleto").send_keys("Juan Prueba")
    navegador.find_element(By.ID, "correo").send_keys("juan@correo.com")
    navegador.find_element(By.ID, "verificarCorreo").send_keys("juan@correo.com")
    navegador.find_element(By.ID, "password").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "verificarPassword").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "telefono").send_keys("987654321")

    Select(navegador.find_element(By.ID, "region")).select_by_index(1)
    Select(navegador.find_element(By.ID, "comuna")).select_by_index(1)

    navegador.find_element(By.ID, "terminos").click()
    navegador.find_element(By.XPATH, "//button[normalize-space()='Registrar']").click()

    time.sleep(0.5)
    logs = obtener_logs(navegador)
    assert any("Datos enviados:" in msg for msg in logs), \
        "No se encontró el mensaje 'Datos enviados:' tras el registro exitoso."

def test_registro_sin_aceptar_terminos(navegador, url_base):
    navegador.get(f"{url_base}/registrarUsuario")

    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Registro de usuario')]"))
    )

    navegador.find_element(By.ID, "nombreCompleto").send_keys("Ana Test")
    navegador.find_element(By.ID, "correo").send_keys("ana@correo.com")
    navegador.find_element(By.ID, "verificarCorreo").send_keys("ana@correo.com")
    navegador.find_element(By.ID, "password").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "verificarPassword").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "telefono").send_keys("912345678")
    Select(navegador.find_element(By.ID, "region")).select_by_index(1)
    Select(navegador.find_element(By.ID, "comuna")).select_by_index(1)

    navegador.find_element(By.XPATH, "//button[normalize-space()='Registrar']").click()

    logs = obtener_logs(navegador)
    assert not any("Datos enviados:" in msg for msg in logs), \
        "Se envió el formulario sin aceptar los términos."
