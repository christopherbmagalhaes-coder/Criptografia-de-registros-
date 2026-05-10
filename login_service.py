import sqlite3
import time
from werkzeug.security import check_password_hash  # type: ignore


class LoginService:

    tentativas = {}

    bloqueados = {}

    MAX_TENTATIVAS = 3

    TEMPO_BLOQUEIO = 60

    def autenticar_usuario(self, conexao, login, senha):

        agora = time.time()

        if login in self.bloqueados:

            if agora < self.bloqueados[login]:

                return {
                    "bloqueado": True,
                    "tempo": int(self.bloqueados[login] - agora)
                }

            else:

                del self.bloqueados[login]

        try:

            cursor = conexao.cursor()

            cursor.execute(
                "SELECT id, senha, role FROM usuarios WHERE login = ?",
                (login,)
            )

            resultado = cursor.fetchone()

            if resultado:

                user_id, senha_hash, role = resultado

                if check_password_hash(senha_hash, senha):

                    self.tentativas.pop(login, None)

                    return {
                        "id": user_id,
                        "login": login,
                        "role": role
                    }

            tentativas_atuais = self.tentativas.get(login, 0) + 1

            self.tentativas[login] = tentativas_atuais

            if tentativas_atuais >= self.MAX_TENTATIVAS:

                self.bloqueados[login] = agora + self.TEMPO_BLOQUEIO

                print(f"Usuário {login} bloqueado por 60 segundos")

            return None

        except sqlite3.Error:

            return None