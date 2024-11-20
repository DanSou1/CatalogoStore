const CACHE_NAME = 'mi-cache-v1';

// Archivos esenciales para cachear
const urlsToCache = [
    './',                 // Página principal
    './index.html',       // Archivo HTML principal
    './carrito.html',     // Otro archivo HTML
    './css/main.css',     // Archivo CSS
    './js/carrito.js',    // Script carrito
    './js/main.js',       // Script principal
    './js/menu.js',       // Script para el menú
];

// Instalar el Service Worker y cachear los archivos esenciales
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('Archivos esenciales cacheados');
            return cache.addAll(urlsToCache);
        })
    );
});

// Interceptar solicitudes
self.addEventListener('fetch', event => {
    const requestUrl = new URL(event.request.url);

    // Cacheo dinámico de imágenes en la carpeta "images"
    if (requestUrl.pathname.startsWith('/img/')) {
        event.respondWith(
            caches.match(event.request).then(cachedResponse => {
                if (cachedResponse) {
                    return cachedResponse; // Devuelve la imagen cacheada
                }
                return fetch(event.request).then(networkResponse => {
                    return caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, networkResponse.clone()); // Almacena la imagen en caché
                        return networkResponse;
                    });
                });
            })
        );
        return;
    }

    // Manejo de otros recursos (estáticos)
    event.respondWith(
        caches.match(event.request).then(cachedResponse => {
            return cachedResponse || fetch(event.request);
        })
    );
});

// Activar el Service Worker y limpiar cachés antiguas
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Caché antiguo eliminado:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
