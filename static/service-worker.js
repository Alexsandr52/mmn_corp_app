const cacheName = 'mm_sup_app-cache-v1';
const resourcesToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/images/upc.svg',
    '/static/images/data_matrix.jpeg',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png',
    '/manifest.json'
];

// Слушатель события install
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(cacheName).then((cache) => {
            return cache.addAll(resourcesToCache);
        })
    );
});

// Слушатель события fetch
self.addEventListener('fetch', (event) => {
    // Кэширование изображений
    if (event.request.url.includes('/static/images/')) {
        event.respondWith(
            caches.open('barcode-images').then((cache) => 
                cache.match(event.request).then((response) =>
                    response || fetch(event.request).then((fetchResponse) => {
                        cache.put(event.request, fetchResponse.clone());
                        return fetchResponse;
                    })
                )
            )
        );
    } else {
        // Обработка других запросов с fallback на сеть
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                return cachedResponse || fetch(event.request);
            })
        );
    }
});
