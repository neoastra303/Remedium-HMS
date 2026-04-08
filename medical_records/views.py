from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import PatientDocument
from patients.models import Patient


class PatientDocumentListView(LoginRequiredMixin, generic.ListView):
    model = PatientDocument
    template_name = 'medical_records/patient_document_list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        self.patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return PatientDocument.objects.filter(patient=self.patient)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context


class PatientDocumentCreateView(LoginRequiredMixin, generic.CreateView):
    model = PatientDocument
    fields = ['document_type', 'title', 'file', 'notes']
    template_name = 'medical_records/patient_document_form.html'

    def form_valid(self, form):
        form.instance.patient = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('patient_document_list', kwargs={'patient_pk': self.kwargs['patient_pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = get_object_or_404(Patient, pk=self.kwargs['patient_pk'])
        return context
