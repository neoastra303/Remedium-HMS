
/**
 * Remedium HMS - June 2026 UX Enhancements
 * Includes: Global Search (Ctrl+K), Page Transitions, Visual Feedback
 */

(function() {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ── 1. Global Search Logic ──────────────────────────────────────────
    const searchModalEl = document.getElementById('globalSearchModal');
    const searchInput = document.getElementById('globalSearchInput');
    const searchResults = document.getElementById('searchResults');
    const searchTrigger = document.getElementById('globalSearchTrigger');

    if (searchModalEl && searchInput && searchResults) {
        const searchModal = new bootstrap.Modal(searchModalEl);

        // Ctrl+K to open search
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                searchModal.show();
            }
        });

        if (searchTrigger) {
            searchTrigger.addEventListener('click', () => searchModal.show());
        }

        // Focus input when modal opens
        searchModalEl.addEventListener('shown.bs.modal', () => {
            searchInput.focus();
        });

        // Handle search input with debounce
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            clearTimeout(searchTimeout);

            if (query.length < 2) {
                searchResults.innerHTML = `
                    <div class="p-4 text-center text-muted">
                        <i class="bi bi-keyboard fs-1 d-block mb-2 opacity-25"></i>
                        <p class="mb-0">Type to search Remedium...</p>
                    </div>`;
                return;
            }

            searchTimeout = setTimeout(() => executeGlobalSearch(query), 300);
        });

        async function executeGlobalSearch(query) {
            searchResults.innerHTML = `
                <div class="p-4 text-center">
                    <div class="spinner-border spinner-border-sm text-primary" role="status"></div>
                    <p class="mt-2 text-muted small">Searching records...</p>
                </div>`;

            try {
                const basePath = searchTrigger
                    ? searchTrigger.getAttribute('data-search-url') || ''
                    : '';
                const [patientsRes, staffRes] = await Promise.all([
                    fetch(`${basePath}/api/v1/patients/?search=${encodeURIComponent(query)}`).then(r => r.json().catch(() => ({}))),
                    fetch(`${basePath}/api/v1/staff/?search=${encodeURIComponent(query)}`).then(r => r.json().catch(() => ({})))
                ]);

                renderSearchResults(patientsRes.results || patientsRes.data || [], staffRes.results || staffRes.data || [], basePath);
            } catch (error) {
                console.error('Search failed:', error);
                searchResults.innerHTML = `<div class="p-4 text-center text-danger small">Error connecting to search service.</div>`;
            }
        }

        function renderSearchResults(patients, staff, basePath) {
            if (patients.length === 0 && staff.length === 0) {
                searchResults.innerHTML = `<div class="p-4 text-center text-muted">No records found for "${searchInput.value}"</div>`;
                return;
            }

            let html = '';

            if (patients.length > 0) {
                html += `<div class="search-category-header">Patients</div>`;
                patients.slice(0, 5).forEach(p => {
                    html += `
                        <a href="${basePath}/patients/${p.id}/" class="search-result-item">
                            <i class="bi bi-person-circle text-primary"></i>
                            <div>
                                <div class="fw-bold">${AJAXHelpers ? AJAXHelpers.escapeHTML(p.first_name + ' ' + p.last_name) : (p.first_name || '') + ' ' + (p.last_name || '')}</div>
                                <div class="small text-muted">${p.unique_id || ''} • ${p.gender || ''}</div>
                            </div>
                            <span class="search-shortcut-hint">Patient</span>
                        </a>`;
                });
            }

            if (staff.length > 0) {
                html += `<div class="search-category-header">Staff</div>`;
                staff.slice(0, 5).forEach(s => {
                    html += `
                        <a href="${basePath}/staff/${s.id}/" class="search-result-item">
                            <i class="bi bi-person-badge text-info"></i>
                            <div>
                                <div class="fw-bold">${AJAXHelpers ? AJAXHelpers.escapeHTML(s.first_name + ' ' + s.last_name) : (s.first_name || '') + ' ' + (s.last_name || '')}</div>
                                <div class="small text-muted">${s.role || ''} • ${s.department || 'General'}</div>
                            </div>
                            <span class="search-shortcut-hint">Staff</span>
                        </a>`;
                });
            }

            searchResults.innerHTML = html;
        }
    }

    // ── 2. Page Transitions ─────────────────────────────────────────────
    if (!prefersReducedMotion) {
        document.querySelectorAll('a').forEach(link => {
            if (link.hostname === window.location.hostname && 
                !link.getAttribute('data-bs-toggle') && 
                !link.href.includes('logout') &&
                !link.href.includes('#') &&
                !link.getAttribute('target') &&
                !link.classList.contains('no-transition')) {
                
                link.addEventListener('click', function(e) {
                    if (e.ctrlKey || e.shiftKey || e.metaKey || e.button !== 0) return;
                    
                    e.preventDefault();
                    const target = this.href;
                    
                    document.body.classList.add('page-transitioning');
                    
                    setTimeout(() => {
                        window.location.href = target;
                    }, 200);
                });
            }
        });
    }

    // ── 3. Visual Feedback Helper ──────────────────────────────────────
    window.applyShake = function(elementId) {
        if (prefersReducedMotion) return;
        const el = document.getElementById(elementId);
        if (el) {
            el.classList.add('haptic-shake');
            setTimeout(() => el.classList.remove('haptic-shake'), 400);
        }
    };

    // Auto-apply blurred zoom on page load (skip if reduced motion)
    if (!prefersReducedMotion) {
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.classList.add('animate-blurred-zoom-in');
        }
    }

})();
