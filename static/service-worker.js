self.addEventListener('install', (event) => {
    event.waitUntil(
      caches.open('mm_sup_app-cache').then((cache) => {
        return cache.addAll([
          '/',
          '/static/css/style.css',
          '/static/js/app.js',
          '/static/images/upc.svg',
          '/static/images/data_matrix.jpeg',
          '/static/icons/icon-192x192.png',
          '/static/icons/icon-512x512.png',
          '/manifest.json'
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        return cachedResponse || fetch(event.request);
      })
    );
  });
  