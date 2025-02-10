from django.db import migrations
from django.db.models import Count

def clean_cpfs(apps, schema_editor):
    Cliente = apps.get_model('clientes', 'Cliente')
    
    # Primeiro, vamos lidar com CPFs vazios
    clientes_sem_cpf = Cliente.objects.filter(cpf__in=[None, ''])
    for cliente in clientes_sem_cpf:
        cliente.cpf = f'SEM_CPF_{cliente.id}'
        cliente.save()
    
    # Agora, vamos lidar com CPFs duplicados
    cpfs_duplicados = Cliente.objects.values('cpf').annotate(total=Count('id')).filter(total__gt=1)
    for cpf_info in cpfs_duplicados:
        cpf = cpf_info['cpf']
        clientes = Cliente.objects.filter(cpf=cpf).order_by('id')
        for i, cliente in enumerate(clientes[1:], start=1):
            cliente.cpf = f'{cpf}_{i}'
            cliente.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0003_fill_empty_cpfs'),
    ]

    operations = [
        migrations.RunPython(clean_cpfs),
    ]

