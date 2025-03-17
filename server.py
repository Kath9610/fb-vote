from flask import Flask, jsonify
import threading

app = Flask(__name__)

def ejecutar_script():
    print("Ejecutando script en el servidor...")

@app.route('/ejecutar', methods=['GET'])
def ejecutar():
    threading.Thread(target=ejecutar_script).start()
    return jsonify({"mensaje": "Script iniciado"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
