const CACHE_NAME = 'hubban-lughat-v52';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './1782975618016.png',
  './manifest.json',
  './tailwind.js'
];

// Install: Cache essential assets individually so failure of one does not reject installation
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      for (const asset of ASSETS_TO_CACHE) {
        try {
          await cache.add(asset);
        } catch (e) {
          console.warn('Asset caching deferred:', asset, e);
        }
      }
      try {
        await cache.add('./words.js?v=52');
      } catch (e) {
        console.warn('words.js caching deferred:', e);
      }
    })
  );
});

// Activate: Clean old caches and take immediate control
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
// - HTML: Instant startup from Cache! (0ms wait, eliminates red splash screen freeze). Background revalidates.
// - words.js: Cache-First with ignoreSearch (instant 10ms memory/disk read).
// - Static Assets: Stale-While-Revalidate
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isHTML = event.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.pathname.endsWith('/');
  const isWordsJs = url.pathname.endsWith('words.js');

  if (isHTML) {
    // Instant launch: Serve cached HTML immediately if available!
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        const fetchPromise = fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        }).catch(() => null);

        if (cachedResponse) {
          return cachedResponse;
        }

        return fetchPromise.then((netRes) => {
          if (netRes && netRes.status === 200) return netRes;
          return caches.match('./index.html').then(r => r || caches.match('./'));
        });
      })
    );
  } else if (isWordsJs) {
    // Cache-First with ignoreSearch: Always load instantaneously from disk
    event.respondWith(
      caches.match(event.request, { ignoreSearch: true }).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(event.request, responseClone);
            });
          }
          return networkResponse;
        }).catch(() => {
          return caches.match('./words.js', { ignoreSearch: true });
        });
      })
    );
  } else {
    // Stale-While-Revalidate for images, icons, manifest
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
