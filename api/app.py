from flask import Flask, jsonify, render_template_string
from config import Config
from models import db
from routes import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(api)

    @app.route("/health")
    def health():
        return jsonify({"status": "ok", "service": "fintrack-api"})

    @app.route("/")
    def index():
        routes = sorted(
            [(str(r.rule), ",".join(sorted(r.methods - {"HEAD", "OPTIONS"}))) for r in app.url_map.iter_rules() if "static" not in r.endpoint]
        )
        return render_template_string(
            """<!doctype html>
            <html>
              <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width,initial-scale=1">
                <title>Fintrack API</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
              </head>
              <body class="bg-light">
                <nav class="navbar navbar-dark bg-dark mb-4">
                  <div class="container">
                    <a class="navbar-brand" href="/">Fintrack API</a>
                    <span class="navbar-text text-muted">Servicio en /api</span>
                  </div>
                </nav>
                <main class="container">
                  <div class="row g-4">
                    <div class="col-12 col-md-6">
                      <div class="card shadow-sm">
                        <div class="card-body">
                          <h5 class="card-title">Estado</h5>
                          <p class="card-text">Comprueba el estado del servicio:</p>
                          <a href="/health" class="btn btn-primary">/health</a>
                        </div>
                      </div>
                    </div>
                    <div class="col-12 col-md-6">
                      <div class="card shadow-sm">
                        <div class="card-body">
                          <h5 class="card-title">Documentación rápida</h5>
                          <p class="card-text">Rutas principales:</p>
                          <ul class="list-unstyled mb-0">
                            <li><a href="/api/categories">/api/categories</a> (GET / POST)</li>
                            <li><a href="/api/transactions?user_id=1">/api/transactions?user_id=1</a> (GET)</li>
                            <li><a href="/api/users/1">/api/users</a> (GET / POST)</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>

                  <footer class="mt-4 mb-4 text-muted small">
                    <p>Fintrack API · ejecutando en Flask</p>
                  </footer>
                </main>
              </body>
            </html>""",
            routes=routes,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)