from django.db import migrations, models
import decimal

class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),  # Update this to the name of your last existing migration
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='frete',
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal('0.00'), max_digits=10),
        ),
    ]

