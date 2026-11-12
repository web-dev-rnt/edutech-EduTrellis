/*
 * Lightweight pjax-style navigation for the admin panel.
 *
 * Clicking a same-origin link inside .admin-root fetches the target page and
 * swaps in its .admin-sidebar and .admin-main instead of doing a full browser
 * navigation, so the sidebar/topbar don't flash and scroll position/open
 * dropdown state isn't lost. Form submissions are untouched (still normal
 * full-page POSTs).
 *
 * Many admin page scripts wrap their setup in
 * document.addEventListener('DOMContentLoaded', fn) — that event only fires
 * once for the real page load, so after an AJAX swap those scripts would
 * silently never run. While re-executing a swapped-in page's <script> tags,
 * we temporarily patch document.addEventListener so a 'DOMContentLoaded'
 * registration is invoked immediately instead of queued, since the DOM it
 * needs is already in place by the time the script runs.
 */
(function () {
  'use strict';

  var currentAbortController = null;
  // Timers started by the currently-loaded page's own scripts (setInterval for a
  // live clock, polling, etc.), so they can be torn down before the next page's
  // content replaces the elements they were updating.
  var pageIntervals = [];
  var pageTimeouts = [];

  function clearPageTimers() {
    pageIntervals.forEach(function (id) { clearInterval(id); });
    pageTimeouts.forEach(function (id) { clearTimeout(id); });
    pageIntervals = [];
    pageTimeouts = [];
  }

  function initSidebarDropdowns(root) {
    root.querySelectorAll('.admin-dropdown').forEach(function (item) {
      item.addEventListener('click', function (e) {
        e.preventDefault();
        var submenu = this.nextElementSibling;
        if (submenu) {
          var open = submenu.style.display !== 'flex';
          submenu.style.display = open ? 'flex' : 'none';
          this.classList.toggle('admin-open', open);
        }
      });
    });
  }

  function bindMobileSidebarClose(root) {
    root.querySelectorAll('a:not(.admin-dropdown)').forEach(function (link) {
      link.addEventListener('click', function () {
        if (window.innerWidth > 900) return;
        var sidebarAtClick = document.querySelector('.admin-sidebar');
        if (!sidebarAtClick || !sidebarAtClick.classList.contains('mobile-open')) return;
        // Close directly instead of re-dispatching overlay.click(): by the time this
        // timeout fires the AJAX nav may have already swapped in a fresh sidebar that
        // never had 'mobile-open', so re-checking that class here would wrongly no-op.
        setTimeout(function () {
          var sidebar = document.querySelector('.admin-sidebar');
          var overlay = document.getElementById('sidebarOverlay');
          var toggleBtn = document.getElementById('mobileMenuBtn');
          if (sidebar) sidebar.classList.remove('mobile-open');
          if (overlay) overlay.classList.remove('active');
          if (toggleBtn) toggleBtn.classList.remove('hidden');
          document.body.style.overflow = '';
        }, 100);
      });
    });
  }

  function executeScripts(container) {
    var originalAdd = document.addEventListener;
    var originalSetInterval = window.setInterval;
    var originalSetTimeout = window.setTimeout;

    document.addEventListener = function (type, listener) {
      if (type === 'DOMContentLoaded') {
        try { listener(); } catch (err) { console.error('[admin-nav] injected script error:', err); }
        return;
      }
      return originalAdd.apply(document, arguments);
    };
    window.setInterval = function () {
      var id = originalSetInterval.apply(window, arguments);
      pageIntervals.push(id);
      return id;
    };
    window.setTimeout = function () {
      var id = originalSetTimeout.apply(window, arguments);
      pageTimeouts.push(id);
      return id;
    };

    try {
      var scripts = Array.prototype.slice.call(container.querySelectorAll('script'));
      scripts.forEach(function (oldScript) {
        var newScript = document.createElement('script');
        Array.prototype.forEach.call(oldScript.attributes, function (attr) {
          newScript.setAttribute(attr.name, attr.value);
        });
        // Wrapped in an IIFE so a page's top-level const/let/class/function
        // declarations don't leak into the shared global lexical scope, where a
        // second page reusing the same name (e.g. two pages each declaring
        // `const _s = ...`) would otherwise throw "already been declared" the
        // next time that page's script is re-executed after an AJAX nav.
        newScript.textContent = '(function () {\n' + oldScript.textContent + '\n})();';
        oldScript.parentNode.replaceChild(newScript, oldScript);
      });
    } finally {
      document.addEventListener = originalAdd;
      window.setInterval = originalSetInterval;
      window.setTimeout = originalSetTimeout;
    }
  }

  // Nodes a page adds to <head> via {% block extra_css %}, found between the two marker metas.
  function pageStyleNodes(doc) {
    var start = doc.querySelector('meta[name="admin-page-styles"][content="start"]');
    var end = doc.querySelector('meta[name="admin-page-styles"][content="end"]');
    var nodes = [];
    if (!start || !end) return null;
    for (var node = start.nextSibling; node && node !== end; node = node.nextSibling) nodes.push(node);
    return { start: start, end: end, nodes: nodes };
  }

  // Replace the current page's head styles with the next page's. Resolves once any new
  // <link rel="stylesheet"> has loaded, so content is never shown unstyled.
  function syncPageStyles(doc) {
    var current = pageStyleNodes(document);
    var next = pageStyleNodes(doc);
    if (!current || !next) return Promise.resolve();

    var pending = [];
    next.nodes.forEach(function (node) {
      var clone;
      if (node.nodeType === 1 && node.tagName === 'LINK') {
        clone = document.createElement('link');
        Array.prototype.forEach.call(node.attributes, function (a) { clone.setAttribute(a.name, a.value); });
        if ((clone.rel || '').toLowerCase() === 'stylesheet') {
          pending.push(new Promise(function (resolve) {
            clone.addEventListener('load', resolve);
            clone.addEventListener('error', resolve);
            setTimeout(resolve, 3000);
          }));
        }
      } else {
        clone = document.importNode(node, true);
      }
      current.end.parentNode.insertBefore(clone, current.end);
    });
    return Promise.all(pending).then(function () {
      current.nodes.forEach(function (node) { if (node.parentNode) node.parentNode.removeChild(node); });
    });
  }

  function swapContent(html, url, pushState) {
    var doc = new DOMParser().parseFromString(html, 'text/html');
    var newMain = doc.querySelector('.admin-main');
    var currentMain = document.querySelector('.admin-main');

    if (!newMain || !currentMain || !pageStyleNodes(doc)) {
      // Not an admin page built on the shared layout (e.g. redirected to login) - do a real navigation.
      window.location.href = url;
      return Promise.resolve();
    }
    return syncPageStyles(doc).then(function () { applySwap(doc, url, pushState); });
  }

  function applySwap(doc, url, pushState) {
    var newSidebar = doc.querySelector('.admin-sidebar');
    var newMain = doc.querySelector('.admin-main');
    var newTitle = doc.querySelector('title');
    var newScripts = doc.getElementById('admin-page-scripts');

    var currentSidebar = document.querySelector('.admin-sidebar');
    var currentMain = document.querySelector('.admin-main');
    var currentScripts = document.getElementById('admin-page-scripts');

    clearPageTimers();

    if (newSidebar && currentSidebar) {
      currentSidebar.replaceWith(newSidebar);
      initSidebarDropdowns(newSidebar);
      bindMobileSidebarClose(newSidebar);
    }

    currentMain.innerHTML = newMain.innerHTML;
    if (newTitle) document.title = newTitle.textContent;

    executeScripts(currentMain);

    // Page scripts from {% block extra_js %} live outside .admin-main.
    if (currentScripts) {
      currentScripts.innerHTML = newScripts ? newScripts.innerHTML : '';
      executeScripts(currentScripts);
    }

    if (pushState) {
      history.pushState({ adminNav: true }, '', url);
    }

    window.scrollTo(0, 0);
    document.dispatchEvent(new CustomEvent('admin:nav-loaded', { detail: { url: url } }));
  }

  function navigateTo(url, pushState) {
    if (currentAbortController) currentAbortController.abort();
    currentAbortController = new AbortController();

    document.body.classList.add('admin-nav-loading');
    fetch(url, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      signal: currentAbortController.signal
    })
      .then(function (resp) {
        if (!resp.ok) throw new Error('Request failed: ' + resp.status);
        return resp.text();
      })
      .then(function (html) {
        return swapContent(html, url, pushState !== false);
      })
      .catch(function (err) {
        if (err.name === 'AbortError') return;
        console.error('[admin-nav] navigation failed, falling back to full load:', err);
        window.location.href = url;
      })
      .finally(function () {
        document.body.classList.remove('admin-nav-loading');
      });
  }

  function isEligibleLink(link) {
    if (!link) return false;
    if (link.target && link.target !== '_self') return false;
    if (link.hasAttribute('download')) return false;
    if (link.dataset.noAjax !== undefined) return false;
    var href = link.getAttribute('href');
    if (!href || href === '#' || href.charAt(0) === '#') return false;
    if (href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) return false;
    if (link.origin !== window.location.origin) return false;
    return true;
  }

  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var link = e.target.closest('a');
    if (!link || !link.closest('.admin-root') || link.classList.contains('admin-dropdown')) return;
    if (!isEligibleLink(link)) return;

    e.preventDefault();
    navigateTo(link.href, true);
  });

  window.addEventListener('popstate', function () {
    navigateTo(window.location.href, false);
  });

  document.addEventListener('DOMContentLoaded', function () {
    var sidebar = document.querySelector('.admin-sidebar');
    if (sidebar) {
      initSidebarDropdowns(sidebar);
      bindMobileSidebarClose(sidebar);
    }
  });

  window.adminNav = { navigateTo: navigateTo };
})();
