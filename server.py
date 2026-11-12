from math import isfinite

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html", peso="", estatura="", resultado=None, error=None)


@app.route("/calcular", methods=["POST"])
def calcular():
    peso_texto = request.form.get("peso", "").strip().replace(",", ".")
    estatura_texto = request.form.get("estatura", "").strip().replace(",", ".")
    resultado = None
    error = None

    try:
        peso = float(peso_texto)
        estatura_cm = float(estatura_texto)
        if not isfinite(peso) or not isfinite(estatura_cm) or peso <= 0 or estatura_cm <= 0:
            raise ValueError
    except ValueError:
        error = "Ingresa un peso y una estatura válidos, mayores que cero."
    else:
        imc = peso / (estatura_cm / 100) ** 2
        if imc < 18.5:
            categoria = "Bajo peso"
        elif imc < 25:
            categoria = "Peso saludable"
        elif imc < 30:
            categoria = "Sobrepeso"
        else:
            categoria = "Obesidad"
        resultado = {"imc": f"{imc:.1f}", "categoria": categoria}

    return render_template(
        "index.html",
        peso=request.form.get("peso", ""),
        estatura=request.form.get("estatura", ""),
        resultado=resultado,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)