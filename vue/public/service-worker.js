const CACHE_NAME = 'anonymiser-pdf-v1';
const urlsToCache = [
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.0.943/pdf.min.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
  );
});