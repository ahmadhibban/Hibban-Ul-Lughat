const CACHE_NAME = 'hubban-lughat-v19';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './1782975618016.png',
  './manifest.json',
  './tailwind.js'
];

// Install: Cache essential assets immediately
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      await cache.addAll(ASSETS_TO_CACHE);
      try {
        await cache.add('./words.js');
      } catch (e) {
        console.warn('words.js caching deferred:', e);
      }
    })
  );
});

// Activate: Clean old caches and take control
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Strategy:
// - HTML & words.js: Network-First with cache fallback (guarantees instant live updates when online, 100% offline fallback)
// - Static Assets: Stale-While-Revalidate
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isHTML = event.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname.endsWith('/');
  const isDynamicAsset = url.pathname.endsWith('words.js') || url.searchParams.has('v');

  if (isHTML || isDynamicAsset) {
    // Network-First for HTML and dictionary data
    event.respondWith(
      fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      }).catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          if (isHTML) return caches.match('./index.html');
          return caches.match('./words.js');
        });
      })
    );
  } else {
    // Stale-While-Revalidate for CSS/Images/Icons
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        const networkFetch = fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        }).catch(() => cachedResponse);

        return cachedResponse || networkFetch;
      })
    );
  }
});
