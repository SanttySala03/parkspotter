# routes/auth_routes.py

from flask import Blueprint, request, jsonify
from db import get_db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)

# --------- REGISTRO ----------
@auth.route("/register", methods=["POST"])
def register():
    data = request.json
    nombre = data.get("nombre")
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "error": "Campos incompletos"}), 400

    hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO usuarios (nombre, email, password)
            VALUES (%s, %s, %s)
        """, (nombre, email, hashed_pw))

        conn.commit()
        return jsonify({"success": True, "msg": "Usuario registrado exitosamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        cur.close()
        conn.close()


# --------- LOGIN ----------
@auth.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM usuarios WHERE email = %s", (email,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if not result:
        return jsonify({"success": False, "error": "Usuario no encontrado"}), 404

    user_id, hashed_pw = result

    if bcrypt.check_password_hash(hashed_pw, password):
        return jsonify({
            "success": True,
            "msg": "Login exitoso",
            "user_id": user_id
        })
    else:
        return jsonify({"success": False, "error": "Contraseña incorrecta"}), 401
