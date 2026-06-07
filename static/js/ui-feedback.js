/**
 * UI feedback helpers:
 * - Form submission spinner on any form with data-spinner
 * - Delete confirmation toast after successful delete redirect
 */

document.addEventListener('DOMContentLoaded', function () {

    // ── Form submission spinner ──────────────────────────────────────────
    // Add data-spinner to any <form> to get automatic submit feedback.
    // The submit button must have data-loading-text attribute.
    document.querySelectorAll('form[data-spinner]').forEach(function (form) {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('[type="submit"]');
            if (!btn) return;
            const textEl = btn.querySelector('[data-submit-text]');
            const spinEl = btn.querySelector('[data-submit-spinner]');
            if (textEl) textEl.classList.add('d-none');
            if (spinEl) spinEl.classList.remove('d-none');
            btn.disabled = true;
        });
    });

    // ── Generic spinner for ALL forms (fallback) ─────────────────────────
    // Any submit button with class btn-primary gets a spinner on submit.
    document.querySelectorAll('form').forEach(function (form) {
        if (form.dataset.spinner) return; // already handled above
        form.addEventListener('submit', function () {
            const btn = form.querySelector('button[type="submit"].btn-primary');
            if (!btn || btn.disabled) return;
            const original = btn.innerHTML;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Please wait…';
            btn.disabled = true;
            // Re-enable after 8s in case of validation failure
            setTimeout(function () {
                btn.innerHTML = original;
                btn.disabled = false;
            }, 8000);
        });
    });

    // ── Delete success toast ─────────────────────────────────────────────
    // Show a toast if URL has ?deleted=1 query param (set by delete views).
    const params = new URLSearchParams(window.location.search);
    if (params.get('deleted')) {
        showToast('Item deleted successfully.', 'success');
        // Clean URL
        const url = new URL(window.location);
        url.searchParams.delete('deleted');
        history.replaceState({}, '', url);
    }

    // ── Toast helper ─────────────────────────────────────────────────────
    window.showToast = function (message, type) {
        type = type || 'info';
        const colorMap = { success: 'bg-success', danger: 'bg-danger', info: 'bg-info', warning: 'bg-warning text-dark' };
        const container = document.querySelector('.toast-container') || createToastContainer();
        const id = 'toast-' + Date.now();
        const safeMessage = window.AJAXHelpers ? AJAXHelpers.escapeHTML(message) : String(message).replace(/[&<>"']/g, function (char) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char];
        });
        const html = `
            <div id="${id}" class="toast align-items-center text-white ${colorMap[type] || 'bg-secondary'} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">${safeMessage}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>`;
        container.insertAdjacentHTML('beforeend', html);
        const toastEl = document.getElementById(id);
        new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 }).show();
        toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
    };

    function createToastContainer() {
        const div = document.createElement('div');
        div.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        div.style.zIndex = '9999';
        document.body.appendChild(div);
        return div;
    }

});
