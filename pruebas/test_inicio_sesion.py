from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def _click_boton_login(navegador):
    """
    Intenta ubicar y hacer click en el botón de login de la Navbar.
    Prueba varias rutas: por texto, por aria-label, por icono SVG y
    como último recurso el último botón del nav.
    Incluye scroll + espera clickable; si falla, usa click por JS.
    """
    candidatos = [
        "//nav//*[self::a or self::button][contains(.,'Iniciar sesión')]",
        "//nav//button[@aria-label='Iniciar sesión' or @aria-label='login']",
        "//nav//*[name()='svg']/ancestor::*[self::button or self::a][1]",
        "(//nav//button)[last()]"
    ]
    for xp in candidatos:
        elems = navegador.find_elements(By.XPATH, xp)
        if not elems:
            continue
        btn = elems[0]
        try:
            navegador.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            WebDriverWait(navegador, 5).until(EC.element_to_be_clickable((By.XPATH, xp)))
            btn.click()
            return True
        except Exception:
            try:
                navegador.execute_script("arguments[0].click();", btn)
                return True
            except Exception:
                pass
    return False

def test_modal_inicio_sesion(navegador, url_base):
    # Abre el home
    navegador.get(url_base)

    # Espera a que exista la barra navbar
    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "nav"))
    )

    # Click en el botón de Login 
    assert _click_boton_login(navegador), "No se encontró ningún botón de Login en la Navbar."

    # Espera a que se abra el modal con el título “Iniciar sesión”
    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']//h5[contains(.,'Iniciar sesión')]"))
    )

    # Completa el formulario
    navegador.find_element(By.ID, "formBasicEmail").send_keys("correo@prueba.com")
    navegador.find_element(By.ID, "formBasicPassword").send_keys("ClaveSegura123")
    navegador.find_element(By.XPATH, "//div[@role='dialog']//button[normalize-space()='Iniciar sesión']").click()

    # Verifica que el modal está siga visible
    assert navegador.find_element(By.XPATH, "//div[@role='dialog']").is_displayed()