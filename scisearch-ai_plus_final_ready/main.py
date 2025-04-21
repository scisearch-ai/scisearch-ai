# main.py
import os
from flask import Flask
from app.routes import bp as routes_blueprint  # Blueprint das rotas

# Diretório base (onde está este arquivo)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta de templates e pasta de arquivos estáticos
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

# Registrar todas as rotas do blueprint
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    # Porta definida pelo Render (ou 10000 por padrão)
    port = int(os.environ.get("PORT", 10000))
    # Habilita debug em desenvolvimento; em produção, considere remover debug=True
    app.run(host="0.0.0.0", port=port, debug=True)
