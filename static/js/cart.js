// ===== MANEJO DEL CARRITO EN localStorage =====

const CART_KEY = 'fastfood_cart';

// Lee el carrito guardado (si no existe, devuelve un arreglo vacío)
function getCart() {
    const data = localStorage.getItem(CART_KEY);
    return data ? JSON.parse(data) : [];
}

// Guarda el carrito completo en localStorage
function saveCart(cart) {
    localStorage.setItem(CART_KEY, JSON.stringify(cart));
    updateCartBadge();
}

// Agrega un producto al carrito (o aumenta su cantidad si ya existe)
function addToCart(productId, productName, price) {
    const cart = getCart();
    const existing = cart.find(item => item.id === productId);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id: productId,
            name: productName,
            price: price,
            quantity: 1
        });
    }

    saveCart(cart);
}

// Cambia la cantidad de un producto (usado en la página del carrito)
function updateQuantity(productId, newQuantity) {
    let cart = getCart();

    if (newQuantity <= 0) {
        cart = cart.filter(item => item.id !== productId);
    } else {
        const item = cart.find(item => item.id === productId);
        if (item) item.quantity = newQuantity;
    }

    saveCart(cart);
    if (typeof renderCartPage === 'function') {
        renderCartPage();
    }
}

function removeFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    saveCart(cart);
    if (typeof renderCartPage === 'function') {
        renderCartPage();
    }
}

// Vacía todo el carrito
function clearCart() {
    localStorage.removeItem(CART_KEY);
    updateCartBadge();
    if (typeof renderCartPage === 'function') {
        renderCartPage();
    }
}

// Actualiza el número que aparece en el globito rojo del ícono flotante
function updateCartBadge() {
    const badge = document.getElementById('cart-count');
    if (!badge) return; // Por si acaso el elemento no existe en esta página

    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    badge.textContent = totalItems;
}

// Esto se ejecuta automáticamente en CADA página que carga este script
document.addEventListener('DOMContentLoaded', updateCartBadge);