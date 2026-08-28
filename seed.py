from app import create_app
from extensions import db
from models import Category, Product

app = create_app()

def seed_data():
    with app.app_context():
        # Evita duplicar datos si el script se ejecuta más de una vez
        if Category.query.first():
            print("Ya existen datos. No se volvió a sembrar la base de datos.")
            return

        # --- Categorías ---
        hamburguesas = Category(name="Hamburguesas", description="Nuestras hamburguesas clásicas")
        combos = Category(name="Combos", description="Combos completos con bebida")
        salchipapas = Category(name="Salchipapas", description="Papas fritas con salchicha")
        bebidas = Category(name="Bebidas", description="Bebidas frías")
        postres = Category(name="Postres", description="Para el antojo dulce")

        db.session.add_all([hamburguesas, combos, salchipapas, bebidas, postres])
        db.session.commit()  # Se hace commit aquí para que cada categoría ya tenga un id asignado

        # --- Productos ---
        productos = [
            Product(
                category_id=hamburguesas.id,
                name="Hamburguesa Clásica",
                description="Carne, queso, lechuga, tomate y salsa especial.",
                price=12.90,
            ),
            Product(
                category_id=hamburguesas.id,
                name="Hamburguesa Doble",
                description="Doble carne, doble queso, con nuestra salsa especial.",
                price=17.90,
            ),
            Product(
                category_id=combos.id,
                name="Combo Clásico",
                description="Hamburguesa clásica + papas + bebida.",
                price=19.90,
            ),
            Product(
                category_id=salchipapas.id,
                name="Salchipapa Personal",
                description="Papas fritas con salchicha, huevo frito y salsas.",
                price=14.90,
            ),
            Product(
                category_id=bebidas.id,
                name="Coca Cola 500ml",
                description="Bebida gaseosa bien fría.",
                price=3.00,
            ),
            Product(
                category_id=postres.id,
                name="Volcán de Chocolate",
                description="Bizcocho caliente relleno de chocolate derretido.",
                price=8.90,
            ),
        ]

        db.session.add_all(productos)
        db.session.commit()

        print(f"Se crearon {len([hamburguesas, combos, salchipapas, bebidas, postres])} categorías y {len(productos)} productos.")

if __name__ == '__main__':
    seed_data()