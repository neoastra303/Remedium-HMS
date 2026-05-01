import pathlib
f = pathlib.Path('core/tests.py')
txt = f.read_text(encoding='utf-8')
# The test authenticates then hits mark_paid on an already-paid invoice → should be 400
txt = txt.replace(
    "response = api_client.post(f'/api/v1/invoices/{invoice.pk}/mark_paid/')\n        assert response.status_code == status.HTTP_401_UNAUTHORIZED",
    "response = api_client.post(f'/api/v1/invoices/{invoice.pk}/mark_paid/')\n        assert response.status_code == status.HTTP_400_BAD_REQUEST"
)
f.write_text(txt, encoding='utf-8')
print('Done')
