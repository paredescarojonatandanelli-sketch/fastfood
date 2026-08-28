from urllib.parse import quote

def generar_link_whatsapp(order, whatsapp_number):
    """
    Construye un enlace wa.me con el mensaje del pedido ya formateado.
    """
    lineas = [f"Hola, quiero realizar el siguiente pedido:", ""]
    lineas.append(f"Pedido #{order.id:06d}")
    lineas.append("")

    for item in order.items:
        lineas.append(f"{item.quantity}x {item.product_name} - S/ {item.subtotal:.2f}")

    lineas.append("")
    lineas.append(f"Subtotal: S/ {order.subtotal:.2f}")
    lineas.append(f"Delivery: S/ {order.delivery_cost:.2f}")
    lineas.append(f"TOTAL: S/ {order.total:.2f}")
    lineas.append("")
    lineas.append(f"Cliente: {order.customer_name}")
    lineas.append(f"Teléfono: {order.customer_phone}")

    if order.order_type == 'delivery':
        lineas.append(f"Dirección: {order.address}")

    lineas.append(f"Método de pago: {order.payment_method.capitalize()}")

    mensaje = "\n".join(lineas)
    mensaje_codificado = quote(mensaje)

    return f"https://wa.me/{whatsapp_number}?text={mensaje_codificado}"