import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SECRET_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


@app.get("/")
def inicio():
    return jsonify({
        "ok": True,
        "mensaje": "Backend de Clik Ya funcionando"
    })


@app.post("/pedidos")
def crear_pedido():
    datos = request.get_json()

    pedido = {
        "nombre": datos["nombre"],
        "telefono": datos["telefono"],
        "ciudad": datos["ciudad"],
        "direccion": datos["direccion"],
        "producto": datos.get("producto", "Combo de 2 lentes TR90"),
        "cantidad": int(datos["cantidad"]),
        "total": float(datos["total"]),
        "estado": "pendiente"
    }

    resultado = supabase.table("pedidos").insert(pedido).execute()

    return jsonify({
        "ok": True,
        "pedido": resultado.data
    }), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
