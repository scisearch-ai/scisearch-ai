from flask import Flask
import os
from app.routes import bp as routes_blueprint  # Importa o blueprint de rotas

# Obtém o diretório atual deste arquivo
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define o caminho absoluto para a pasta de templates (certifique-se de que ela exista e contenha o index.html)
template_path = os.path.join(current_dir, "templates")

# Cria a aplicação Flask especificando o diretório dos templates
app = Flask(__name__, template_folder=template_path)

# Registra o blueprint que contém as rotas da aplicação
app.register_blueprint(routes_blueprint)

if __name__ == "__main__":
    # Render.com define a porta através da variável de ambiente PORT; se não estiver definida, utiliza 10000.
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
