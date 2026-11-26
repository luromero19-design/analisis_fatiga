# servidor flask
import os
from flask import Flask, render_template, request, jsonify
from calculos import analizar_emg

app = Flask(__name__)

# Carga página principal
@app.route("/")
def index():
    return render_template("index.html")

# Se reciben los datos del formulario
@app.route("/evaluar", methods=["POST"])
def evaluar():
    datos = request.get_json()
    if not datos or "muestras" not in datos:
        return jsonify({"error": "No se recibieron muestras"}), 400

    muestras = [float(x) for x in datos["muestras"] if x is not None]
    if len(muestras) == 0:
        return jsonify({"error": "La lista de muestras está vacía"}), 400

    resultado = analizar_emg(muestras)
    return jsonify(resultado)

# Iniciar servidor
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
