from flask import Flask, jsonify
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tempfile

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")

app = Flask(__name__)

# Variables globales
ejecutando = False
contador_votos = 0  # Contador de votos

def ejecutar_script():
    """Ejecuta el script de votación en un bucle."""
    global ejecutando, contador_votos
    ejecutando = True

    while ejecutando:
        print("Ejecutando script...")
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--start-maximized")
        
        # 🔥 SOLUCIÓN: Asigna un directorio único para cada sesión de Chrome
        chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
        
        # Configura el servicio con la ruta de ChromeDriver
        service = Service('/usr/bin/chromedriver')  # Ruta en Railway
        
        # Instancia el driver con las opciones corregidas
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            driver.get("https://www.thaiupdate.info/the-best-series-of-the-year-final/")
            print("Página cargada correctamente.")

            try:
                boton = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
                )
                boton.click()
                print("✔ Botón de consentimiento clickeado.")
            except:
                print("✔ No se encontró el botón de consentimiento.")

            wait = WebDriverWait(driver, 10)
            label_option = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@for='answer[203]']")))
            driver.execute_script("arguments[0].scrollIntoView();", label_option)
            time.sleep(1)
            label_option.click()
            print("✔ Opción seleccionada.")

            time.sleep(1)
            vote_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'basic-vote-button')]")))
            driver.execute_script("arguments[0].scrollIntoView();", vote_button)
            vote_button.click()
            print("✔ Voto enviado.")

            # Incrementamos el contador
            contador_votos += 1

            time.sleep(5)

        except Exception as e:
            print(f"⚠ Error: {e}")

        finally:
            driver.quit()

        for _ in range(300):
            if not ejecutando:
                print("⏹ Script detenido.")
                return
            time.sleep(1)

@app.route("/")
def home():
    return jsonify({"message": "Bienvenido al servicio de automatización con Selenium."})

@app.route("/start", methods=["GET"])
def start():
    global ejecutando
    if not ejecutando:
        hilo = threading.Thread(target=ejecutar_script, daemon=True)
        hilo.start()
        return jsonify({"status": "Ejecutando"}), 200
    return jsonify({"status": "Ya estaba ejecutándose"}), 400

@app.route("/stop", methods=["GET"])
def stop():
    global ejecutando
    ejecutando = False
    return jsonify({"status": "Detenido"}), 200

@app.route("/count", methods=["GET"])
def count():
    """Devuelve el número de votos realizados."""
    return jsonify({"count": contador_votos})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




