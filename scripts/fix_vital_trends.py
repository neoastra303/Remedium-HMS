import pathlib, re

f = pathlib.Path("care_monitoring/views.py")
txt = f.read_text(encoding="utf-8")

old = txt[txt.find("class PatientVitalTrendsView") :]
new_class = '''class PatientVitalTrendsView(LoginRequiredMixin, PermissionRequiredMixin, generic.View):
    """Redirect to patient detail — vitals chart is embedded in the Vitals tab."""
    permission_required = 'care_monitoring.care_monitoring_view_patientcare'
    raise_exception = True

    def get(self, request, pk):
        from django.shortcuts import redirect
        return redirect('patient_detail', pk=pk)
'''

txt = txt[: txt.find("class PatientVitalTrendsView")] + new_class
f.write_text(txt, encoding="utf-8")
print("Done")
