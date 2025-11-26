# routes/reservas_routes.py

from flask import Blueprint, request, jsonify
from db import get_db

reservas = Blueprint("reservas", __name__)

# CREAR RESERVA
@reservas.route("/reservar", methods=["POST"])
def reservar():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO reservas (usuario_id, parqueadero_id, fecha_inicio, fecha_fin, total_pagar)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data["usuario_id"],
            data["parqueadero_id"],
            data["fecha_inicio"],
            data["fecha_fin"],
            data["total_pagar"]
        ))

        conn.commit()
        return jsonify({"msg": "Reserva creada"})
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cur.close()
        conn.close()


# LISTAR RESERVAS DE UN USUARIO
@reservas.route("/reservas/<int:usuario_id>", methods=["GET"])
def listar_reservas(usuario_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM reservas WHERE usuario_id = %s
    """, (usuario_id,))

    rows = cur.fetchall()
    columnas = [desc[0] for desc in cur.description]
    reservas = [dict(zip(columnas, row)) for row in rows]

    cur.close()
    conn.close()

    return jsonify(reservas)
