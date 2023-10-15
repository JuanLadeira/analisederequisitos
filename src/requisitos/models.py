from django.db import models
from django.core.validators import MinValueValidator
import datetime

# Create your models here.


class MetaModelo(models.Model):
    """'
    Este é o Meta-Modelo que relaciona todos os outros modelos.
    Ele serve como um ponto central para rastrear como os diferentes níveis de informação estão interconectados.
    """
    descricao = models.TextField()


class Ambiental(models.Model):
    """
    Este modelo representa o nível Ambiental na estrutura de rastreamento de requisitos.
    Ele captura os fatores externos e seus impactos associados que podem afetar o projeto.
    """
    meta_modelo = models.ForeignKey(MetaModelo, related_name='ambientais', on_delete=models.CASCADE)
    fator_externo = models.CharField(max_length=255)
    impacto = models.TextField()

class Organizacional(models.Model):
    """
    Este modelo representa o nível Organizacional.
    Ele captura os objetivos e estratégias organizacionais que orientam o projeto.
    """
    meta_modelo = models.ForeignKey(MetaModelo, related_name='organizacionais', on_delete=models.CASCADE)
    objetivo = models.CharField(max_length=255)
    estrategia = models.TextField()

class Gerencial(models.Model):
    """
    Este modelo representa o nível Gerencial na estrutura de rastreamento de requisitos.
    """
    meta_modelo = models.ForeignKey(MetaModelo, related_name='gerenciais', on_delete=models.CASCADE)
    recurso = models.CharField(max_length=255)
    prazo = models.DateField(validators=[MinValueValidator(datetime.date.today)])

    class Meta:
        ordering = ['prazo']

    def __str__(self):
        return self.recurso
    
class Desenvolvimento(models.Model):
    """
    Este modelo representa o nível de Desenvolvimento.
    Ele captura os requisitos funcionais e não funcionais que o sistema deve cumprir.
    """
    meta_modelo = models.ForeignKey(MetaModelo, related_name='desenvolvimentos', on_delete=models.CASCADE)
    requisito_funcional = models.TextField()
    requisito_nao_funcional = models.TextField()

class ModeloIntermediario(models.Model):
    """
    Este modelo serve como um modelo intermediário para capturar informações que são comuns entre diferentes Meta-Modelos.
    """
    meta_modelos = models.ManyToManyField(MetaModelo, related_name='modelos_intermediarios')
    informacao_comum = models.TextField()

class Tarefa(models.Model):
    """
    Este modelo representa as tarefas individuais associadas a um recurso gerencial.
    Ele captura a descrição da tarefa e seu status atual.
    """
    gerencial = models.ForeignKey(Gerencial, on_delete=models.CASCADE)
    descricao = models.TextField()
    status = models.CharField(max_length=50, choices=[('Pendente', 'Pendente'), ('Concluído', 'Concluído')])
