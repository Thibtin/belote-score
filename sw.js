const CACHE_NAME = 'belote-score-v1';
const ASSETS = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './model/best.onnx',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/lucide@latest',
  'https://cdn.jsdelivr.net/npm/onnxruntime-web/dist/ort.min.js'
];

// Installation : Mise en cache des fichiers et du modèle ONNX
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

// Interception des requêtes : Récupération depuis le cache si hors-ligne
self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});