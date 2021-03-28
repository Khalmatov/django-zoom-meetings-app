from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.db.models import Q

from .models import *
from .tables import *
from .utils import DataMixin



class HomeView(LoginRequiredMixin, DataMixin, TemplateView):
	template_name = 'charis/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Главная'
		c_def = self.get_user_context()
		context = dict(list(context.items()) + list(c_def.items()))
		return context


class SecondCourseView(ExportMixin, DataMixin, SingleTableView):

	table_class = MeetingListTable
	template_name = 'charis/2course.html'

	def get_queryset(self):
		return Meeting.objects.filter(Q(topic__icontains='2 курс')|Q(topic__icontains='харис онлайн'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Второй курс - Харис'
		c_def = self.get_user_context()
		context = dict(list(context.items()) + list(c_def.items()))
		return context


class MeetingListView(ExportMixin, DataMixin, SingleTableView):

	model = Meeting
	table_class = MeetingListTable
	template_name = 'charis/meetings.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Все конференции Zoom'
		c_def = self.get_user_context()
		context = dict(list(context.items()) + list(c_def.items()))
		return context


class MeetingDetailView(ExportMixin, DataMixin, SingleTableView):

	table_class = MeetingDetailTable
	template_name = 'charis/meeting.html'

	def get_queryset(self):
		return Time.objects.select_related('participant').filter(meeting=Meeting.objects.get(uuid=self.kwargs['uuid']))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		meeting = Meeting.objects.get(uuid=self.kwargs['uuid'])
		context['meeting'] = meeting
		context['title'] = 'Конференция: ' + meeting.topic
		c_def = self.get_user_context()
		context = dict(list(context.items()) + list(c_def.items()))
		return context


class ParticipantListView(ExportMixin, DataMixin, SingleTableView):

	model = Participant
	table_class = ParticipantListTable
	template_name = 'charis/participants.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Все участники Zoom'
		c_def = self.get_user_context()
		context = dict(list(context.items()) + list(c_def.items()))
		return context


class ParticipantDetailView(ExportMixin, DataMixin, SingleTableView):
	table_class = ParticipantDetailTable
	template_name = 'charis/participant.html'

	def get_queryset(self):
		return Time.objects.select_related('meeting').filter(participant=Participant.objects.get(id=self.kwargs['id']))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		participant = Participant.objects.get(id=self.kwargs['id'])
		context['participant'] = participant
		context['title'] = participant.name
		c_def = self.get_user_context()
		context = dict(list(context.items()) + list(c_def.items()))
		return context

