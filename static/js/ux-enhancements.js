/**
 * Remedium HMS - UX Enhancements
 * Includes: Global Search (Ctrl+K), Dark Mode, Keyboard Navigation, Toast Dismiss All
 */

(function() {
    'use strict';

    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ── 1. Dark Mode Toggle ────────────────────────────────────────────
    const darkModeToggle = document.getElementById('darkModeToggle');
    const html = document.documentElement;
    const STORAGE_KEY = 'remedium-theme';

    function setTheme(theme) {
        html.setAttribute('data-theme', theme);
        localStorage.setItem(STORAGE_KEY, theme);
        if (darkModeToggle) {
            const icon = darkModeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
            }
            darkModeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
        }
    }

    function initTheme() {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            setTheme(saved);
        } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
        }
    }

    initTheme();

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            const current = html.getAttribute('data-theme');
            setTheme(current === 'dark' ? 'light' : 'dark');
        });
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem(STORAGE_KEY)) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });

    // ── 2. Global Search Logic ──────────────────────────────────────────
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
            searchTrigger.addEventListener('click', function() {
                searchModal.show();
            });
        }

        // Focus input when modal opens
        searchModalEl.addEventListener('shown.bs.modal', function() {
            searchInput.focus();
        });

        // Handle search input with debounce
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            clearTimeout(searchTimeout);

            if (query.length < 2) {
                searchResults.innerHTML = '<div class="p-4 text-center text-muted">' +
                    '<i class="bi bi-keyboard fs-1 d-block mb-2 opacity-25"></i>' +
                    '<p class="mb-0">Type to search Remedium...</p></div>';
                return;
            }

            searchTimeout = setTimeout(function() {
                executeGlobalSearch(query);
            }, 300);
        });

        // Keyboard navigation in search results
        let selectedSearchIndex = -1;
        searchInput.addEventListener('keydown', function(e) {
            const items = searchResults.querySelectorAll('.search-result-item');
            if (!items.length) return;

            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedSearchIndex = Math.min(selectedSearchIndex + 1, items.length - 1);
                updateSearchSelection(items);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedSearchIndex = Math.max(selectedSearchIndex - 1, 0);
                updateSearchSelection(items);
            } else if (e.key === 'Enter' && selectedSearchIndex >= 0) {
                e.preventDefault();
                items[selectedSearchIndex].click();
            }
        });

        function updateSearchSelection(items) {
            items.forEach(function(item, i) {
                item.classList.toggle('selected', i === selectedSearchIndex);
            });
            if (selectedSearchIndex >= 0 && items[selectedSearchIndex]) {
                items[selectedSearchIndex].scrollIntoView({ block: 'nearest' });
            }
        }

        async function executeGlobalSearch(query) {
            searchResults.innerHTML = '<div class="p-4 text-center">' +
                '<div class="spinner-border spinner-border-sm text-primary" role="status"></div>' +
                '<p class="mt-2 text-muted small">Searching records...</p></div>';

            try {
                const basePath = searchTrigger
                    ? searchTrigger.getAttribute('data-search-url') || ''
                    : '';

                const searchPromises = [
                    fetch(basePath + '/api/v1/patients/?search=' + encodeURIComponent(query))
                        .then(function(r) { return r.json().catch(function() { return {}; }); }),
                    fetch(basePath + '/api/v1/staff/?search=' + encodeURIComponent(query))
                        .then(function(r) { return r.json().catch(function() { return {}; }); }),
                    fetch(basePath + '/api/v1/appointments/?search=' + encodeURIComponent(query))
                        .then(function(r) { return r.json().catch(function() { return {}; }); }),
                    fetch(basePath + '/api/v1/invoices/?search=' + encodeURIComponent(query))
                        .then(function(r) { return r.json().catch(function() { return {}; }); }),
                    fetch(basePath + '/api/v1/prescriptions/?search=' + encodeURIComponent(query))
                        .then(function(r) { return r.json().catch(function() { return {}; }); })
                ];

                const results = await Promise.all(searchPromises);
                const patients = results[0].results || results[0].data || [];
                const staff = results[1].results || results[1].data || [];
                const appointments = results[2].results || results[2].data || [];
                const invoices = results[3].results || results[3].data || [];
                const prescriptions = results[4].results || results[4].data || [];

                renderSearchResults(patients, staff, appointments, invoices, prescriptions, basePath);
            } catch (error) {
                console.error('Search failed:', error);
                searchResults.innerHTML = '<div class="p-4 text-center text-danger small">Error connecting to search service.</div>';
            }
        }

        function renderSearchResults(patients, staff, appointments, invoices, prescriptions, basePath) {
            var totalResults = patients.length + staff.length + appointments.length + invoices.length + prescriptions.length;

            if (totalResults === 0) {
                searchResults.innerHTML = '<div class="p-4 text-center text-muted">No records found for "' + escapeHtml(searchInput.value) + '"</div>';
                return;
            }

            var html = '';

            if (patients.length > 0) {
                html += '<div class="search-category-header">Patients</div>';
                patients.slice(0, 5).forEach(function(p) {
                    var name = (p.first_name || '') + ' ' + (p.last_name || '');
                    html += '<a href="' + basePath + '/patients/' + p.id + '/" class="search-result-item">' +
                        '<i class="bi bi-person-circle text-primary"></i>' +
                        '<div><div class="fw-bold">' + escapeHtml(name) + '</div>' +
                        '<div class="small text-muted">' + escapeHtml(p.unique_id || '') + ' &bull; ' + escapeHtml(p.gender || '') + '</div></div>' +
                        '<span class="search-shortcut-hint">Patient</span></a>';
                });
            }

            if (staff.length > 0) {
                html += '<div class="search-category-header">Staff</div>';
                staff.slice(0, 5).forEach(function(s) {
                    var name = (s.first_name || '') + ' ' + (s.last_name || '');
                    html += '<a href="' + basePath + '/staff/' + s.id + '/" class="search-result-item">' +
                        '<i class="bi bi-person-badge text-info"></i>' +
                        '<div><div class="fw-bold">' + escapeHtml(name) + '</div>' +
                        '<div class="small text-muted">' + escapeHtml(s.role || '') + ' &bull; ' + escapeHtml(s.department || 'General') + '</div></div>' +
                        '<span class="search-shortcut-hint">Staff</span></a>';
                });
            }

            if (appointments.length > 0) {
                html += '<div class="search-category-header">Appointments</div>';
                appointments.slice(0, 3).forEach(function(a) {
                    var patientName = a.patient_name || (a.patient_first_name || '') + ' ' + (a.patient_last_name || '');
                    html += '<a href="' + basePath + '/appointments/' + a.id + '/" class="search-result-item">' +
                        '<i class="bi bi-calendar-event text-warning"></i>' +
                        '<div><div class="fw-bold">' + escapeHtml(patientName) + '</div>' +
                        '<div class="small text-muted">' + escapeHtml(a.status || '') + ' &bull; ' + escapeHtml(a.appointment_date || '') + '</div></div>' +
                        '<span class="search-shortcut-hint">Appointment</span></a>';
                });
            }

            if (invoices.length > 0) {
                html += '<div class="search-category-header">Invoices</div>';
                invoices.slice(0, 3).forEach(function(inv) {
                    var patientName = inv.patient_name || '';
                    html += '<a href="' + basePath + '/invoices/' + inv.id + '/" class="search-result-item">' +
                        '<i class="bi bi-receipt text-success"></i>' +
                        '<div><div class="fw-bold">' + escapeHtml(patientName) + '</div>' +
                        '<div class="small text-muted">$' + escapeHtml(String(inv.total_amount || '0')) + ' &bull; ' + (inv.paid ? 'Paid' : 'Unpaid') + '</div></div>' +
                        '<span class="search-shortcut-hint">Invoice</span></a>';
                });
            }

            if (prescriptions.length > 0) {
                html += '<div class="search-category-header">Prescriptions</div>';
                prescriptions.slice(0, 3).forEach(function(rx) {
                    var patientName = rx.patient_name || '';
                    html += '<a href="' + basePath + '/prescriptions/' + rx.id + '/" class="search-result-item">' +
                        '<i class="bi bi-capsule text-danger"></i>' +
                        '<div><div class="fw-bold">' + escapeHtml(patientName) + '</div>' +
                        '<div class="small text-muted">' + escapeHtml(rx.medication_name || rx.status || '') + '</div></div>' +
                        '<span class="search-shortcut-hint">Rx</span></a>';
                });
            }

            searchResults.innerHTML = html;
            selectedSearchIndex = -1;
        }

        function escapeHtml(str) {
            var div = document.createElement('div');
            div.appendChild(document.createTextNode(str || ''));
            return div.innerHTML;
        }
    }

    // ── 3. Toast Dismiss All ────────────────────────────────────────────
    function updateDismissAllButton() {
        var container = document.getElementById('toastContainer');
        var dismissBtn = document.getElementById('toastDismissAll');
        if (!container || !dismissBtn) return;

        var toasts = container.querySelectorAll('.toast');
        if (toasts.length > 1) {
            dismissBtn.classList.add('visible');
        } else {
            dismissBtn.classList.remove('visible');
        }
    }

    var toastDismissAllBtn = document.getElementById('toastDismissAll');
    if (toastDismissAllBtn) {
        toastDismissAllBtn.addEventListener('click', function() {
            var container = document.getElementById('toastContainer');
            if (!container) return;
            container.querySelectorAll('.toast.show').forEach(function(toastEl) {
                var instance = bootstrap.Toast.getInstance(toastEl);
                if (instance) instance.hide();
            });
        });
    }

    // Monitor toast additions
    var toastObserver = new MutationObserver(function() {
        updateDismissAllButton();
    });
    var toastContainer = document.getElementById('toastContainer');
    if (toastContainer) {
        toastObserver.observe(toastContainer, { childList: true });
    }

    // ── 4. Keyboard Table Navigation ───────────────────────────────────
    document.addEventListener('keydown', function(e) {
        // Only when not in an input/select/textarea
        if (['INPUT', 'SELECT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;
        if (e.target.closest('.modal')) return;

        var tables = document.querySelectorAll('.table');
        if (!tables.length) return;

        var activeTable = null;
        var rows = [];

        tables.forEach(function(table) {
            var tableRows = table.querySelectorAll('tbody tr');
            if (tableRows.length) {
                var rect = table.getBoundingClientRect();
                if (rect.top < window.innerHeight && rect.bottom > 0) {
                    activeTable = table;
                    rows = Array.from(tableRows);
                }
            }
        });

        if (!activeTable) return;

        var selectedRow = activeTable.querySelector('tbody tr.kb-selected');
        var currentIndex = selectedRow ? rows.indexOf(selectedRow) : -1;

        if (e.key === 'j' || e.key === 'ArrowDown') {
            e.preventDefault();
            var nextIndex = currentIndex < rows.length - 1 ? currentIndex + 1 : 0;
            selectRow(rows, nextIndex);
        } else if (e.key === 'k' || e.key === 'ArrowUp') {
            e.preventDefault();
            var prevIndex = currentIndex > 0 ? currentIndex - 1 : rows.length - 1;
            selectRow(rows, prevIndex);
        } else if (e.key === 'Enter' && selectedRow) {
            var link = selectedRow.querySelector('a[href]');
            if (link) link.click();
        }
    });

    function selectRow(rows, index) {
        rows.forEach(function(r) { r.classList.remove('kb-selected'); });
        rows[index].classList.add('kb-selected');
        rows[index].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }

    // ── 5. Visual Feedback Helper ──────────────────────────────────────
    window.applyShake = function(elementId) {
        if (prefersReducedMotion) return;
        var el = document.getElementById(elementId);
        if (el) {
            el.classList.add('haptic-shake');
            setTimeout(function() { el.classList.remove('haptic-shake'); }, 400);
        }
    };

    // Auto-apply blurred zoom on page load (skip if reduced motion)
    if (!prefersReducedMotion) {
        var mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.classList.add('animate-blurred-zoom-in');
        }
    }

})();
