from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0006_historicalinvoice_invoice_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="InvoiceCounter",
            fields=[
                ("year", models.PositiveIntegerField(primary_key=True, serialize=False)),
                ("last_seq", models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
