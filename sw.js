const CACHE_NAME = 'belote-score-v1';

// Liste des fichiers à mettre en cache
const ASSETS = [
  'index.html',
  'style.css',
  'app.js',
  'model/best.onnx',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // ignoreSearch: true pour éviter les problèmes de requêtes
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
