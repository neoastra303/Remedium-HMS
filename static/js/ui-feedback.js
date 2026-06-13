document.addEventListener('DOMContentLoaded', function () {

    // ── Form submission spinner ──────────────────────────────────────
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

    // ── Generic spinner fallback ────────────────────────────────────
    document.querySelectorAll('form:not([data-spinner])').forEach(function (form) {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('button[type="submit"].btn-primary');
            if (!btn || btn.disabled) return;
            const original = btn.innerHTML;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Please wait\u2026';
            btn.disabled = true;
            setTimeout(function () {
                btn.innerHTML = original;
                btn.disabled = false;
            }, 8000);
        });
    });

    // ── Delete success toast ────────────────────────────────────────
    const params = new URLSearchParams(window.location.search);
    if (params.get('deleted')) {
        showToast('Item deleted successfully.', 'success');
        const url = new URL(window.location);
        url.searchParams.delete('deleted');
        history.replaceState({}, '', url);
    }

    if (params.get('created')) {
        showToast('Item created successfully.', 'success');
        const url = new URL(window.location);
        url.searchParams.delete('created');
        history.replaceState({}, '', url);
    }

    if (params.get('updated')) {
        showToast('Item updated successfully.', 'success');
        const url = new URL(window.location);
        url.searchParams.delete('updated');
        history.replaceState({}, '', url);
    }

    // ── Toast helper with stacking ──────────────────────────────────
    window.showToast = function (message, type) {
        type = type || 'info';
        const colorMap = {
            success: 'bg-success',
            danger: 'bg-danger',
            error: 'bg-danger',
            info: 'bg-info',
            warning: 'bg-warning text-dark'
        };
        const container = document.getElementById('toastContainer') || createToastContainer();
        const id = 'toast-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6);
        const safeMessage = window.AJAXHelpers
            ? AJAXHelpers.escapeHTML(message)
            : String(message).replace(/[&<>"']/g, function (char) {
                return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char];
              });
        const html = [
            '<div id="' + id + '" class="toast align-items-center text-white ' + (colorMap[type] || 'bg-secondary') + ' border-0 animate-fade-in" role="alert" aria-live="assertive" aria-atomic="true">',
            '<div class="d-flex">',
            '<div class="toast-body">',
            '<i class="bi bi-' + (type === 'success' ? 'check-circle-fill' : type === 'danger' || type === 'error' ? 'exclamation-circle-fill' : type === 'warning' ? 'exclamation-triangle-fill' : 'info-circle-fill') + ' me-1"></i>',
            safeMessage,
            '</div>',
            '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>',
            '</div>',
            '</div>'
        ].join('');
        container.insertAdjacentHTML('beforeend', html);
        const toastEl = document.getElementById(id);
        const toast = new bootstrap.Toast(toastEl, { autohide: true, delay: 4000 });
        toast.show();
        toastEl.addEventListener('hidden.bs.toast', function () {
            if (toastEl.parentNode) toastEl.parentNode.removeChild(toastEl);
        });
        // Limit visible toasts to 3, remove oldest
        const visible = container.querySelectorAll('.toast.show');
        if (visible.length > 3) {
            for (let i = 0; i < visible.length - 3; i++) {
                const oldToast = bootstrap.Toast.getInstance(visible[i]);
                if (oldToast) oldToast.hide();
            }
        }
    };

    function createToastContainer() {
        const div = document.createElement('div');
        div.id = 'toastContainer';
        div.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(div);
        return div;
    }

});
