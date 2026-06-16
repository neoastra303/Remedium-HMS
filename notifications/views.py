from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Notification


class NotificationListView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.ListView
):
    model = Notification
    template_name = "notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = 20
    ordering = ["-sent_at"]
    permission_required = "notifications.view_notification"
    raise_exception = True


@login_required
@permission_required("notifications.change_notification", raise_exception=True)
@require_POST
def mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.status = "SENT"
    notification.save(update_fields=["status"])
    messages.success(request, "Notification marked as read.")
    return redirect("notification_list")


@login_required
@permission_required("notifications.change_notification", raise_exception=True)
@require_POST
def mark_all_read(request):
    Notification.objects.filter(status="PENDING").update(status="SENT")
    messages.success(request, "All notifications marked as read.")
    return redirect("notification_list")
