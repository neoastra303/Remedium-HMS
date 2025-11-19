from django.shortcuts import render
from django.views import generic
from .forms import LabTestForm
from .models import LabTest
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class LabTestListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = LabTest
    template_name = 'laboratory/labtest_list.html'
    context_object_name = 'lab_tests'
    paginate_by = 10  # Add pagination
    permission_required = 'laboratory.laboratory_view_labtest'
    raise_exception = True

    def get_queryset(self):
        queryset = super().get_queryset()
        order_by = self.request.GET.get('order_by', 'requested_date') # Default sort by requested_date
        return queryset.order_by(order_by)


class LabTestDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = LabTest
    template_name = 'laboratory/labtest_detail.html'
    context_object_name = 'lab_test'
    permission_required = 'laboratory.laboratory_view_labtest'
    raise_exception = True


class LabTestCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = LabTest
    form_class = LabTestForm
    template_name = 'laboratory/labtest_form.html'
    success_url = reverse_lazy('labtest_list')
    permission_required = 'laboratory.laboratory_add_labtest'
    raise_exception = True


class LabTestUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    model = LabTest
    form_class = LabTestForm
    success_url = reverse_lazy('labtest_list')
    permission_required = 'laboratory.laboratory_change_labtest'
    raise_exception = True


class LabTestDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = LabTest
    template_name = 'laboratory/labtest_confirm_delete.html'
    success_url = reverse_lazy('labtest_list')
    permission_required = 'laboratory.laboratory_delete_labtest'
    raise_exception = True

# Create your views here.