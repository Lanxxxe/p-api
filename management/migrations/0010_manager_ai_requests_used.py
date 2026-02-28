from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_remove_photos_from_internshiplog'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='ai_requests_used',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
