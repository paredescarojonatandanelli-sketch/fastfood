from extensions import db
from models import Category, Product

def run_seed():
    if Category.query.first():
        print("Ya existen datos. No se volvio a sembrar la base de datos.")
        return

    hamburguesas = Category(name="Hamburguesas", description="Nuestras hamburguesas clasicas")
    combos = Category(name="Combos", description="Combos completos con bebida")
    salchipapas = Category(name="Salchipapas", description="Papas fritas con salchicha")
    bebidas = Category(name="Bebidas", description="Bebidas frias")
    postres = Category(name="Postres", description="Para el antojo dulce")

    db.session.add_all([hamburguesas, combos, salchipapas, bebidas, postres])
    db.session.commit()

    productos = [
        Product(category_id=hamburguesas.id, name="Hamburguesa Clasica", description="Carne, queso, lechuga, tomate y salsa especial.", price=12.90, image="hamburguesa-clasica.jpg"),
        Product(category_id=hamburguesas.id, name="Hamburguesa Doble", description="Doble carne, doble queso, con nuestra salsa especial.", price=17.90, image="hamburguesa-doble.jpg"),
        Product(category_id=combos.id, name="Combo Clasico", description="Hamburguesa clasica + papas + bebida.", price=19.90),
        Product(category_id=salchipapas.id, name="Salchipapa Personal", description="Papas fritas con salchicha, huevo frito y salsas.", price=14.90, image="salchipapa.jpg"),
        Product(category_id=bebidas.id, name="Coca Cola 500ml", description="Bebida gaseosa bien fria.", price=3.00, image="coca-cola.jpg"),
        Product(category_id=postres.id, name="Volcan de Chocolate", description="Bizcocho caliente relleno de chocolate derretido.", price=8.90, image="volcan-chocolate.jpg"),
    ]

    db.session.add_all(productos)
    db.session.commit()
    print(f"Se sembraron {len(productos)} productos correctamente.")