import threading
import time
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Variable global para controlar la ejecución del script
ejecutando = False  
hilo = None

def ejecutar_script():
    """Ejecuta el script en un bucle cada 5 minutos sin mostrar el navegador."""
    global ejecutando
    ejecutando = True

    while ejecutando:
        print("Ejecutando script...")

        # 🔹 Configurar Selenium en modo invisible (headless) 🔹
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--disable-extensions")  
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  
        chrome_options.add_argument("--start-maximized")

        # Iniciar el navegador sin necesidad de ruta local de ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get("https://www.thaiupdate.info/the-best-series-of-the-year-final/")
            print("Página cargada correctamente.")

            # Manejar el botón de consentimiento si aparece
            try:
                boton = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "fc-button.fc-cta-consent.fc-primary-button"))
                )
                boton.click()
                print("✔ Botón de consentimiento clickeado.")
            except:
                print("✔ No se encontró el botón de consentimiento (puede que no sea necesario).")

            # Seleccionar opción de votación
            wait = WebDriverWait(driver, 10)
            label_option = wait.until(EC.presence_of_element_located((By.XPATH, "//label[@for='answer[203]']")))
            driver.execute_script("arguments[0].scrollIntoView();", label_option)
            time.sleep(1)
            label_option.click()
            print("✔ Opción 'The Loyal Pin' seleccionada.")

            # Hacer clic en "VOTE"
            time.sleep(1)
            vote_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'basic-vote-button')]")))
            driver.execute_script("arguments[0].scrollIntoView();", vote_button)
            vote_button.click()
            print("✔ Voto enviado con éxito.")

            time.sleep(5)  # Esperar antes de cerrar

        except Exception as e:
            print(f"⚠ Error: {e}")

        finally:
            driver.quit()

        # Esperar 5 minutos antes de la siguiente ejecución
        print("⌛ Esperando 5 minutos antes de la próxima ejecución...\n")
        for _ in range(300):  # 300 segundos = 5 minutos
            if not ejecutando:
                print("⏹ Script detenido.")
                return
            time.sleep(1)

@app.route('/start', methods=['GET'])
def iniciar():
    """Inicia el script en un hilo separado."""
    global ejecutando, hilo
    if not ejecutando:
        hilo = threading.Thread(target=ejecutar_script, daemon=True)
        hilo.start()
        return jsonify({"message": "🟢 Script iniciado."})
    return jsonify({"message": "⚠ El script ya está en ejecución."})

@app.route('/stop', methods=['GET'])
def detener():
    """Detiene la ejecución del script."""
    global ejecutando
    ejecutando = False
    return jsonify({"message": "🔴 Script detenido."})

@app.route('/')
def home():
    return jsonify({"message": "Bienvenido al servicio de automatización con Selenium."})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


