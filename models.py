from django.db import models
from django.shortcuts import reverse

class Student(models.Model):

	name = models.CharField('Имя', max_length=255)
	email = models.EmailField('Почта', null=True, blank=True)
	login_at = models.DateTimeField('Время входа')
	logout_at = models.DateTimeField('Время выхода')
	time = models.IntegerField('Время сеанса')
	is_guest = models.CharField('Гость?', max_length=10)


class Meeting(models.Model):

	uuid = models.CharField(primary_key=True, max_length=100)
	id = models.BigIntegerField(unique=False)
	topic = models.CharField('Название конференции', max_length=255)
	start_time = models.DateTimeField('Начало')
	end_time = models.DateTimeField('Конец')
	duration = models.IntegerField('Продолжительность')
	total_minutes = models.IntegerField('Всего минут')

	def __str__(self):
		return self.topic

	def get_absolute_url(self):
		return reverse('meeting', kwargs={'uuid':self.uuid})

	class Meta:
		verbose_name='Конференция'
		verbose_name_plural='Конференции'


class Participant(models.Model):

	id = models.BigIntegerField(primary_key=True)
	name = models.CharField('Имя', max_length=255)
	user_email = models.EmailField('E-mail', null=True, blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('participant', kwargs={'id':self.id})

	class Meta:
		verbose_name='Участник'
		verbose_name_plural='Участники'
		ordering = ('name',)


class Time(models.Model):
	"""Хранит время проведенное участником конференции"""

	meeting = models.ForeignKey('Meeting', on_delete=models.CASCADE, verbose_name='Конференция')
	participant = models.ForeignKey('Participant', on_delete=models.CASCADE, verbose_name='Участник')
	join_time = models.DateTimeField('Подключение')
	leave_time = models.DateTimeField('Отключение')
	duration = models.IntegerField('Продолжительность')

	def __str__(self):
		return self.participant.name

	class Meta:
		default_related_name = 'times'