from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cliente',
            options={'ordering': ['nome']},
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='email',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='endereco',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='telefone',
        ),
        migrations.AddField(
            model_name='cliente',
            name='bairro',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cidade',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='numero',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='obs',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='rua',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefone1',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='telefone2',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='cliente',
            name='uf',
            field=models.CharField(blank=True, default='', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='nome',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]

