# routes/parqueaderos_routes.py

from flask import Blueprint, request, jsonify
from db import get_db

parqueaderos = Blueprint("parqueaderos", __name__)

# CREAR PARQUEADERO
@parqueaderos.route("/parqueaderos", methods=["POST"])
def crear_parqueadero():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO parqueaderos 
            (propietario_id, titulo, descripcion, direccion, latitud, longitud, precio_hora)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["propietario_id"],
            data["titulo"],
            data["descripcion"],
            data["direccion"],
            data["latitud"],
            data["longitud"],
            data["precio_hora"]
        ))

        conn.commit()
        return jsonify({"msg": "Parqueadero creado"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur.close()
        conn.close()


# LISTAR PARQUEADEROS DISPONIBLES
@parqueaderos.route("/parqueaderos", methods=["GET"])
def listar_parqueaderos():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM parqueaderos WHERE disponible = TRUE")
    parqueaderos = cur.fetchall()

    columnas = [desc[0] for desc in cur.description]
    data = [dict(zip(columnas, row)) for row in parqueaderos]

    cur.close()
    conn.close()

    return jsonify(data)
