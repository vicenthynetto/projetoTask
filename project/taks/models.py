from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=250, blank=True)
    description = models.CharField(max_length=250, blank=True)
    due_date = models.DateField(blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    status = models.BooleanField('Ativo?', default=True)