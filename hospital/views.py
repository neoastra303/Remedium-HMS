from django.shortcuts import render
from django.views import generic
from .models import Ward, Room
from .forms import WardForm, RoomForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class WardListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Ward
    template_name = 'hospital/ward_list.html'
    context_object_name = 'wards'
    paginate_by = 10
    permission_required = 'hospital.view_ward'

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'name')
        return queryset.order_by(order_by)


class WardDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Ward
    template_name = 'hospital/ward_detail.html'
    context_object_name = 'ward'
    permission_required = 'hospital.view_ward'


class WardCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Ward
    form_class = WardForm
    template_name = 'hospital/ward_form.html'
    success_url = reverse_lazy('ward_list')
    permission_required = 'hospital.add_ward'


class WardUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Ward
    form_class = WardForm
    template_name = 'hospital/ward_form.html'
    success_url = reverse_lazy('ward_list')
    permission_required = 'hospital.change_ward'


class WardDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Ward
    template_name = 'hospital/ward_confirm_delete.html'
    success_url = reverse_lazy('ward_list')
    permission_required = 'hospital.delete_ward'


class RoomListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Room
    template_name = 'hospital/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 10
    permission_required = 'hospital.view_room'

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'room_number')
        return queryset.order_by(order_by)


class RoomDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Room
    template_name = 'hospital/room_detail.html'
    context_object_name = 'room'
    permission_required = 'hospital.view_room'


class RoomCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'hospital/room_form.html'
    success_url = reverse_lazy('room_list')
    permission_required = 'hospital.add_room'


class RoomUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'hospital/room_form.html'
    success_url = reverse_lazy('room_list')
    permission_required = 'hospital.change_room'


class RoomDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Room
    template_name = 'hospital/room_confirm_delete.html'
    success_url = reverse_lazy('room_list')
    permission_required = 'hospital.delete_room'