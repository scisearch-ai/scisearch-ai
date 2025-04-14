from flask import Flask, render_template
import os

# Obtém o diretório atual deste arquivo
current_dir = os.path.dirname(os.path.abspath(__file__))

# Define o caminho absoluto para a pasta de templates (assegure-se de que esta pasta exista e contenha o index.html)
template_path = os.path.join(current_dir, "templates")

# Cria a aplicação Flask especificando o diretório dos templates
app = Flask(__name__, template_folder=template_path)

# Exemplo de opções que serão passadas para o template (ajuste conforme necessário)
FILTER_OPTIONS = ['Opção 1', 'Opção 2', 'Opção 3']

@app.route("/")
def index():
    return render_template("index.html", filter_options=FILTER_OPTIONS)

if __name__ == "__main__":
    # Render.com define a porta através da variável de ambiente PORT; se não estiver definida, utiliza 10000.
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
