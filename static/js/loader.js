/**
 * Centralized Loader System
 * ==========================
 * Single source of truth for all loading overlay and spinner behaviour.
 * Included globally from base.html so every page can use showLoading() /
 * hideLoading() without duplicating code.
 *
 * Functions exposed on `window`:
 *   - showLoading()           – show the full-page dashboard overlay
 *   - hideLoading()           – hide the full-page dashboard overlay
 *   - showSectionLoader(id)   – show a per-section skeleton loader
 *   - hideSectionLoader(id)   – hide a per-section skeleton loader
 */

(function () {
    'use strict';

    /* ------------------------------------------------------------------
       Full-page loading overlay  (#loadingOverlay)
       Used by dashboards for filter submissions and page transitions.
       ------------------------------------------------------------------ */

    var _overlayTimeout = null;
    var OVERLAY_MAX_MS  = 15000; // safety timeout to prevent infinite spinner

    /**
     * Show the full-page loading overlay.
     * Automatically hides after OVERLAY_MAX_MS as a safety net.
     */
    function showLoading() {
        var overlay = document.getElementById('loadingOverlay');
        if (!overlay) return;

        // Clear any pending hide timer
        if (_overlayTimeout) {
            clearTimeout(_overlayTimeout);
            _overlayTimeout = null;
        }

        overlay.style.display  = 'flex';
        overlay.style.opacity  = '1';

        // Safety: auto-hide after timeout to prevent infinite spinner
        _overlayTimeout = setTimeout(function () {
            hideLoading();
        }, OVERLAY_MAX_MS);
    }

    /**
     * Hide the full-page loading overlay with a smooth fade-out.
     */
    function hideLoading() {
        var overlay = document.getElementById('loadingOverlay');
        if (!overlay) return;

        if (_overlayTimeout) {
            clearTimeout(_overlayTimeout);
            _overlayTimeout = null;
        }

        overlay.style.opacity = '0';
        setTimeout(function () {
            overlay.style.display = 'none';
        }, 300);
    }

    /* ------------------------------------------------------------------
       Section-level loaders
       Ready for future lazy-loading: each dashboard section can have a
       <div id="loader-<sectionKey>" class="section-loader"> placeholder.
       ------------------------------------------------------------------ */

    /**
     * Show a per-section skeleton loader.
     * @param {string} sectionId – DOM id of the section container
     */
    function showSectionLoader(sectionId) {
        var container = document.getElementById(sectionId);
        if (!container) return;

        // Don't insert duplicate loaders
        if (container.querySelector('.section-loader')) return;

        var loader = document.createElement('div');
        loader.className = 'section-loader';
        loader.innerHTML =
            '<div class="section-spinner"></div>' +
            '<span>Loading data…</span>' +
            '<div class="skeleton-bar long"></div>' +
            '<div class="skeleton-bar medium"></div>' +
            '<div class="skeleton-bar short"></div>';

        container.prepend(loader);
    }

    /**
     * Hide a per-section skeleton loader.
     * @param {string} sectionId – DOM id of the section container
     */
    function hideSectionLoader(sectionId) {
        var container = document.getElementById(sectionId);
        if (!container) return;

        var loader = container.querySelector('.section-loader');
        if (loader) {
            loader.remove();
        }
    }

    /* ------------------------------------------------------------------
       Auto-hide overlay on page load events
       Covers initial loads, back/forward navigation, and bfcache.
       ------------------------------------------------------------------ */

    // Hide on DOMContentLoaded
    document.addEventListener('DOMContentLoaded', function () {
        setTimeout(hideLoading, 100);
    });

    // Hide on full load (images, iframes, etc.)
    window.addEventListener('load', function () {
        setTimeout(hideLoading, 100);
    });

    // Handle browser back/forward (bfcache)
    window.addEventListener('pageshow', function (event) {
        if (event.persisted) {
            setTimeout(hideLoading, 100);
        }
    });

    // Fallback safety: hide after 2 seconds no matter what
    setTimeout(hideLoading, 2000);

    /* ------------------------------------------------------------------
       Expose to global scope
       ------------------------------------------------------------------ */
    window.showLoading      = showLoading;
    window.hideLoading       = hideLoading;
    window.showSectionLoader = showSectionLoader;
    window.hideSectionLoader = hideSectionLoader;

})();
