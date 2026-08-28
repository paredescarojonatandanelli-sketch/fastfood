import qrcode

def generar_qr(url, ruta_salida='qr_negocio.png'):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color='black', back_color='white')
    imagen.save(ruta_salida)

    print('QR generado correctamente: ' + ruta_salida)


if __name__ == '__main__':
    url_del_negocio = 'https://midominio.com'
    generar_qr(url_del_negocio)
