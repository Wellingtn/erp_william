from django.db import migrations
import uuid

def fill_empty_cpfs(apps, schema_editor):
    Cliente = apps.get_model('clientes', 'Cliente')
    for cliente in Cliente.objects.filter(cpf__in=[None, '']):
        cliente.cpf = str(uuid.uuid4())[:20]  # Gera um identificador único
        cliente.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_alter_cliente_options_remove_cliente_email_and_more'),
    ]

    operations = [
        migrations.RunPython(fill_empty_cpfs),
    ]

