
/**
 * Remedium HMS - June 2026 UX Enhancements
 * Includes: Global Search (Ctrl+K), Page Transitions, Visual Feedback
 */

(function() {
    'use strict';

    // ── 1. Global Search Logic ──────────────────────────────────────────
    const searchModal = new bootstrap.Modal(document.getElementById('globalSearchModal'));
    const searchInput = document.getElementById('globalSearchInput');
    const searchResults = document.getElementById('searchResults');
    const searchTrigger = document.getElementById('globalSearchTrigger');

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
    document.getElementById('globalSearchModal').addEventListener('shown.bs.modal', () => {
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
            // Parallel search across Patients and Staff APIs
            // Note: Adjust URLs based on your actual API structure
            const [patientsRes, staffRes] = await Promise.all([
                fetch(`/api/v1/patients/?search=${encodeURIComponent(query)}`).then(r => r.json()),
                fetch(`/api/v1/staff/?search=${encodeURIComponent(query)}`).then(r => r.json())
            ]);

            renderSearchResults(patientsRes.data || [], staffRes.data || []);
        } catch (error) {
            console.error('Search failed:', error);
            searchResults.innerHTML = `<div class="p-4 text-center text-danger small">Error connecting to search service.</div>`;
        }
    }

    function renderSearchResults(patients, staff) {
        if (patients.length === 0 && staff.length === 0) {
            searchResults.innerHTML = `<div class="p-4 text-center text-muted">No records found for "${searchInput.value}"</div>`;
            return;
        }

        let html = '';

        if (patients.length > 0) {
            html += `<div class="search-category-header">Patients</div>`;
            patients.slice(0, 5).forEach(p => {
                html += `
                    <a href="/patients/${p.id}/" class="search-result-item">
                        <i class="bi bi-person-circle text-primary"></i>
                        <div>
                            <div class="fw-bold">${p.first_name} ${p.last_name}</div>
                            <div class="small text-muted">${p.unique_id} • ${p.gender}</div>
                        </div>
                        <span class="search-shortcut-hint">Patient</span>
                    </a>`;
            });
        }

        if (staff.length > 0) {
            html += `<div class="search-category-header">Staff</div>`;
            staff.slice(0, 5).forEach(s => {
                html += `
                    <a href="/staff/${s.id}/" class="search-result-item">
                        <i class="bi bi-person-badge text-info"></i>
                        <div>
                            <div class="fw-bold">${s.first_name} ${s.last_name}</div>
                            <div class="small text-muted">${s.role} • ${s.department || 'General'}</div>
                        </div>
                        <span class="search-shortcut-hint">Staff</span>
                    </a>`;
            });
        }

        searchResults.innerHTML = html;
    }

    // ── 2. Page Transitions ─────────────────────────────────────────────
    document.querySelectorAll('a').forEach(link => {
        // Only internal links, not data-toggles or logout forms
        if (link.hostname === window.location.hostname && 
            !link.getAttribute('data-bs-toggle') && 
            !link.href.includes('logout') &&
            !link.href.includes('#')) {
            
            link.addEventListener('click', function(e) {
                if (e.ctrlKey || e.shiftKey || e.metaKey) return; // Allow new tab
                
                e.preventDefault();
                const target = this.href;
                
                document.body.classList.add('page-transitioning');
                
                setTimeout(() => {
                    window.location.href = target;
                }, 200);
            });
        }
    });

    // ── 3. Visual Feedback Helper ──────────────────────────────────────
    window.applyShake = function(elementId) {
        const el = document.getElementById(elementId);
        if (el) {
            el.classList.add('haptic-shake');
            setTimeout(() => el.classList.remove('haptic-shake'), 400);
        }
    };

    // Auto-apply blurred zoom on page load
    const mainContent = document.getElementById('main-content');
    if (mainContent) {
        mainContent.classList.add('animate-blurred-zoom-in');
    }

})();
