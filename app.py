from flask import Flask, render_template
from config import Config
from extensions import db
from models import Category, Product, Order, OrderItem
from routes.customer import customer_bp
from routes.admin import admin_bp
from utils.seed_data import run_seed

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
    db.create_all()
    run_seed()

    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))