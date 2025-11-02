import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Helpers
def form_es_valido(driver):
    """True si el <form> pasa HTML5 (required/pattern)."""
    return driver.execute_script("return document.querySelector('form').checkValidity();")

def hay_mensaje_validacion(driver):
    """True si hay inputs inválidos visibles tras intentar enviar."""
    return driver.execute_script("""
        const f = document.querySelector('form');
        if (!f) return false;
        const invalid = f.querySelector(':invalid');
        return !!invalid;
    """)

def js_click(driver, element):
    """Evita ElementClickIntercepted: centra y click por JS."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    driver.execute_script("arguments[0].click();", element)

def campos_invalidos(driver):
    """
    Devuelve una lista con los campos inválidos y su mensaje de validación.
    Úsalo para saber exactamente qué está fallando.
    """
    return driver.execute_script("""
        const f = document.querySelector('form');
        if (!f) return [];
        return Array.from(f.querySelectorAll(':invalid')).map(el => ({
            id: el.id || null,
            name: el.name || null,
            tag: el.tagName,
            type: el.type || null,
            value: el.value || null,
            message: el.validationMessage
        }));
    """)

def seleccionar_opcion_valida(driver, select_id):
    """
    Selecciona la primera opción válida (no deshabilitada y con value no vacío)
    y dispara el evento 'change' por si tu React/Next actualiza la comuna/región.
    """
    driver.execute_script("""
        const s = document.getElementById(arguments[0]);
        if (!s) return;
        const opts = Array.from(s.options);
        const valido = opts.find(o => !o.disabled && o.value && o.value !== '0');
        if (valido) s.value = valido.value;
        s.dispatchEvent(new Event('change', {bubbles:true}));
    """, select_id)

def reglas_telefono(driver):
    """Lee las reglas declaradas del input#telefono (pattern, min/max, title)."""
    return driver.execute_script("""
        const el = document.getElementById('telefono');
        if (!el) return null;
        return {
            pattern: el.pattern || null,
            minLength: el.minLength || null,
            maxLength: el.maxLength || null,
            title: el.title || null,
            type: el.type || null
        };
    """)

def set_telefono_valido(driver):
    """
    Prueba varios formatos típicos de Chile hasta que el form quede válido.
    Si ninguno sirve, lanza error mostrando el pattern/min/max/title reales.
    """
    el = driver.find_element(By.ID, "telefono")
    candidatos = [
        "+56987654321", "56987654321", "987654321",
        "9 8765 4321", "(+56)987654321", "(+56) 9 8765 4321",
        "56 9 8765 4321", "(+56)9-8765-4321", "9-8765-4321",
    ]
    for valor in candidatos:
        el.clear()
        el.send_keys(valor)
        ok = driver.execute_script("return document.getElementById('telefono').checkValidity();")
        if ok:
            return valor  # teléfono aceptado

    # Si nada funcionó, informamos qué pide exactamente el input
    r = reglas_telefono(driver)
    raise AssertionError(f"El teléfono no cumple el patrón del input. Reglas: {r}")

# Tests 
def test_registro_exitoso(navegador, url_base):
    navegador.get(f"{url_base}/registrarUsuario")

    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Registro')]"))
    )

    # Completar campos
    navegador.find_element(By.ID, "nombreCompleto").send_keys("Juan Prueba")
    navegador.find_element(By.ID, "correo").send_keys("juan@correo.com")
    navegador.find_element(By.ID, "verificarCorreo").send_keys("juan@correo.com")
    navegador.find_element(By.ID, "password").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "verificarPassword").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "telefono").send_keys("912345678")

    # Seleccionar región/comuna de 
    seleccionar_opcion_valida(navegador, "region")
    # Si tu comuna depende de la región, se demora un poco
    time.sleep(0.3)
    seleccionar_opcion_valida(navegador, "comuna")

    # Aceptar términos 
    js_click(navegador, navegador.find_element(By.ID, "terminos"))

    # Si aún es inválido, imprime exactamente qué campo falla
    if not form_es_valido(navegador):
        invalid = campos_invalidos(navegador)
        raise AssertionError(f"El formulario no es válido antes del envío. Campos inválidos: {invalid}")

    # Enviar el formulario sin click físico
    navegador.execute_script("document.querySelector('form').requestSubmit();")

    time.sleep(0.5)
    assert not hay_mensaje_validacion(navegador), "Tras enviar, el formulario mostró errores de validación."

def test_registro_sin_aceptar_terminos(navegador, url_base):
    navegador.get(f"{url_base}/registrarUsuario")

    WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[contains(.,'Registro')]"))
    )

    navegador.find_element(By.ID, "nombreCompleto").send_keys("Ana Test")
    navegador.find_element(By.ID, "correo").send_keys("ana@correo.com")
    navegador.find_element(By.ID, "verificarCorreo").send_keys("ana@correo.com")
    navegador.find_element(By.ID, "password").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "verificarPassword").send_keys("ClaveSegura123")
    navegador.find_element(By.ID, "telefono").send_keys("912345678")

    seleccionar_opcion_valida(navegador, "region")
    time.sleep(0.3)
    seleccionar_opcion_valida(navegador, "comuna")

    # No aceptar términos, ya que el formulario debe quedar inválido
    assert not form_es_valido(navegador), "El formulario aparece válido sin aceptar términos."