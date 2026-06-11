self.addEventListener('install', (e) => {
    console.log('[Service Worker] Instalado');
});

self.addEventListener('fetch', (e) => {
    // Apenas deixa a internet passar normalmente para o Supabase
});