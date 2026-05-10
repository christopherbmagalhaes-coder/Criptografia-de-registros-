from flask import Flask, render_template, request, redirect, session
from database import conectar, criar_tabelas, criar_usuarios_teste
from login_service import LoginService
import time

app = Flask(__name__)

app.secret_key = "segredo_super_seguro"

login_service = LoginService()

criar_tabelas()
criar_usuarios_teste()

rate_limit = {}

MAX_REQ = 10
WINDOW = 10


def verificar_rate_limit(ip):

    agora = time.time()

    reqs = rate_limit.get(ip, [])

    reqs = [r for r in reqs if agora - r < WINDOW]

    if len(reqs) >= MAX_REQ:
        return False

    reqs.append(agora)

    rate_limit[ip] = reqs

    return True


def registrar_log(usuario, acao, detalhes, ip):

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO logs (username, action, details, ip, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
        """,
        (usuario, acao, detalhes, ip)
    )

    conexao.commit()

    conexao.close()


@app.route("/", methods=["GET", "POST"])
def login():

    erro = None

    if request.method == "POST":

        ip = request.remote_addr

        if not verificar_rate_limit(ip):

            registrar_log(
                "ANONIMO",
                "LIMITE_REQUISICOES_IP",
                "IP bloqueado",
                ip
            )

            erro = "Muitas tentativas. Aguarde."

            return render_template(
                "login.html",
                erro=erro
            )

        usuario_login = request.form["username"]

        senha = request.form["password"]

        conexao = conectar()

        user = login_service.autenticar_usuario(
            conexao,
            usuario_login,
            senha
        )

        conexao.close()

        if user and not user.get("bloqueado"):

            session["user"] = user["login"]

            session["role"] = user["role"]

            registrar_log(
                usuario_login,
                "LOGIN_SUCESSO",
                "Login realizado com sucesso",
                ip
            )

            return redirect("/dashboard")

        elif user and user.get("bloqueado"):

            registrar_log(
                usuario_login,
                "USUARIO_BLOQUEADO",
                "Tentativa de login bloqueada",
                ip
            )

            erro = (
                f"Usuário bloqueado. "
                f"Aguarde {user['tempo']} segundos."
            )

        else:

            registrar_log(
                usuario_login,
                "LOGIN_FALHA",
                "Falha no login",
                ip
            )

            erro = "Login inválido"

    return render_template(
        "login.html",
        erro=erro
    )


@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        registrar_log(
            "ANONIMO",
            "TENTATIVA_SEM_LOGIN",
            "Tentativa de acesso ao dashboard sem login",
            request.remote_addr
        )

        return redirect("/")

    return render_template(
        "dashboard.html",
        user=session["user"],
        role=session["role"]
    )


@app.route("/admin")
def admin():

    if "user" not in session:

        registrar_log(
            "ANONIMO",
            "TENTATIVA_SEM_LOGIN",
            "Tentativa de acesso ao admin sem login",
            request.remote_addr
        )

        return redirect("/")

    if session["role"] != "admin":

        registrar_log(
            session["user"],
            "ACESSO_NEGADO",
            "Tentativa de acesso à área admin",
            request.remote_addr
        )

        return redirect("/acesso_negado")

    registrar_log(
        session["user"],
        "ACESSO_ADMIN_AUTORIZADO",
        "Acesso autorizado à área admin",
        request.remote_addr
    )

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("SELECT login, role FROM usuarios")

    users = [
        {
            "username": u[0],
            "role": u[1]
        }
        for u in cursor.fetchall()
    ]

    cursor.execute(
        """
        SELECT username, action, details, ip, created_at
        FROM logs
        ORDER BY id DESC
        """
    )

    logs = [
        {
            "username": l[0],
            "action": l[1],
            "details": l[2],
            "ip": l[3],
            "created_at": l[4]
        }
        for l in cursor.fetchall()
    ]

    conexao.close()

    return render_template(
        "admin.html",
        users=users,
        logs=logs
    )


@app.route("/registros", methods=["GET", "POST"])
def registros():

    if "user" not in session:

        registrar_log(
            "ANONIMO",
            "TENTATIVA_SEM_LOGIN",
            "Tentativa de acesso aos registros sem login",
            request.remote_addr
        )

        return redirect("/")

    registrar_log(
        session["user"],
        "ACESSO_REGISTROS",
        "Acesso à página de registros",
        request.remote_addr
    )

    conexao = conectar()

    cursor = conexao.cursor()

    erro = None

    if request.method == "POST":

        try:

            material = request.form["material"]

            tipo_recurso = request.form["tipo_recurso"]

            valor = request.form["valor_emergetico"]

            data = request.form["data_registro"]

            usuario = session["user"]

            cursor.execute(
                """
                INSERT INTO registros
                (material, tipo_recurso, valor_emergetico,
                 data_registro, criado_por)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    material,
                    tipo_recurso,
                    valor,
                    data,
                    usuario
                )
            )

            conexao.commit()

            registrar_log(
                usuario,
                "REGISTRO_CRIADO",
                "Novo registro emergético criado",
                request.remote_addr
            )

        except Exception:

            erro = "Erro ao salvar registro"

    cursor.execute(
        """
        SELECT material,
               tipo_recurso,
               valor_emergetico,
               data_registro,
               criado_por
        FROM registros
        ORDER BY id DESC
        """
    )

    registros = [
        {
            "material": r[0],
            "tipo_recurso": r[1],
            "valor_emergetico": r[2],
            "data_registro": r[3],
            "criado_por": r[4]
        }
        for r in cursor.fetchall()
    ]

    conexao.close()

    return render_template(
        "registros.html",
        registros=registros,
        user=session["user"],
        role=session["role"],
        erro=erro
    )


@app.route("/acesso_negado")
def acesso_negado():

    usuario = session.get("user", "ANONIMO")

    registrar_log(
        usuario,
        "ACESSO_NEGADO",
        "Redirecionado para página de acesso negado",
        request.remote_addr
    )

    return render_template("acesso_negado.html")


@app.route("/logout")
def logout():

    usuario = session.get("user", "ANONIMO")

    registrar_log(
        usuario,
        "LOGOUT",
        "Usuário saiu do sistema",
        request.remote_addr
    )

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(debug=True)