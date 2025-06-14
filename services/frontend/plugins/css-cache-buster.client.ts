export default defineNuxtPlugin(() => {
  if (process.dev) {
    // Force reload CSS files on every navigation
    const bustCSS = () => {
      const links = document.querySelectorAll('link[rel="stylesheet"]');
      links.forEach((link) => {
        if (link instanceof HTMLLinkElement && link.href) {
          const url = new URL(link.href);
          url.searchParams.set('v', Date.now().toString());
          link.href = url.toString();
        }
      });
    };

    // Bust CSS cache immediately
    if (process.client) {
      setTimeout(bustCSS, 100);
      
      // Also bust on router navigation
      const router = useRouter();
      router.afterEach(() => {
        setTimeout(bustCSS, 50);
      });
      
      // Listen for page reloads
      window.addEventListener('beforeunload', bustCSS);
      
      // Watch for new CSS being added
      const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
          mutation.addedNodes.forEach((node) => {
            if (node instanceof HTMLLinkElement && node.rel === 'stylesheet') {
              const url = new URL(node.href);
              url.searchParams.set('v', Date.now().toString());
              node.href = url.toString();
            }
          });
        });
      });
      
      observer.observe(document.head, { childList: true });
    }
  }
}); 