from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '12345'

    from app.managers.papers.routes import papers_bp
    app.register_blueprint(papers_bp)

    from app.managers.doing_now.routes import doing_now_bp
    app.register_blueprint(doing_now_bp)

    from app.managers.description.routes import description_bp
    app.register_blueprint(description_bp)

    from app.managers.summary.routes import summary_bp
    app.register_blueprint(summary_bp)

    return app
