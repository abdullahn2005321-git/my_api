from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from db import init_db, get_conn
import sqlite3
import os
from users_routes import users_bp


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me-32chars!!")
jwt = JWTManager(app)

@app.get("/")
def home():
    return "Hello Abdullah", 200

@app.get("/health")
def health():
    return jsonify(status="ok"), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Route not found", path=request.path), 404

@app.post("/register")
def register():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="send JSON body"), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not isinstance(username, str) or username.strip() == "":
        return jsonify(error="username is required"), 400
    if not password or not isinstance(password, str) or len(password) < 4:
        return jsonify(error="password must be least 4 chars"), 400
    
    username = username.strip()
    password_hash = generate_password_hash(password)

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO auth_users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify(error="username already exists"), 409
    

    new_id = cur.lastrowid
    conn.close()
    return jsonify(user={"id": new_id, "username": username}), 201



@app.post("/login")
def login():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="send JSON body"), 400
    
    username = data.get("username")
    password = data.get("password")

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash FROM auth_users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row is None or not check_password_hash(row["password_hash"], password or ""):
        return jsonify(error="Invalid username or password"), 401

    token = create_access_token(
        identity=str(row["id"]),
        additional_claims={"username": row["username"]}
    )
    return jsonify(token=token, token_type="Bearer"), 200

@app.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify(user={
        "id": int(user_id),
        "username": claims.get("username")
    }), 200

app.register_blueprint(users_bp)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
