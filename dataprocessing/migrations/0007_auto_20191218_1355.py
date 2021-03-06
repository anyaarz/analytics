# Generated by Django 2.0.5 on 2019-12-18 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataprocessing', '0006_auto_20191216_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='item1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item1', to='dataprocessing.Items', verbose_name='Элемент РПД №1'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='item2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item2', to='dataprocessing.Items', verbose_name='Элемент РПД №2'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='relation',
            field=models.CharField(choices=[('0', 'неопределенное'), ('1', 'включает в себя'), ('2', 'является пререквизитом'), ('3', 'тождество'), ('4', 'являются частями одного раздела'), ('5', 'отсутствует')], default='0', max_length=10, verbose_name='Связь'),
        ),
    ]
