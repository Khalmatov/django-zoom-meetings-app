import django_tables2 as tables
from .models import *


class ParticipantListTable(tables.Table):
	name = tables.LinkColumn()
	class Meta:
		model = Participant
		exclude = ('id',)
		attrs = {"class": "table table-striped table-borderless table-sm"}
		empty_text = 'В таблице нет данных'

class ParticipantDetailTable(tables.Table):
	meeting = tables.LinkColumn()

	class Meta:
		model = Time
		exclude = ('id', 'participant')
		order_by = ('join_time',)
		attrs = {"class": "table table-striped table-borderless table-sm"}
		empty_text = 'В таблице нет данных'

	def render_duration(self, value):
		return f'{value//60}  минут'


class MeetingListTable(tables.Table):
	topic = tables.LinkColumn()

	class Meta:
		model = Meeting
		exclude = ('uuid', 'id')
		order_by = ('-start_time',)
		attrs = {"class": "table table-striped table-borderless table-sm"}
		empty_text = 'В таблице нет данных'

	def render_duration(self, value):
		return f'{value} минут'


class MeetingDetailTable(tables.Table):
	participant = tables.LinkColumn()

	class Meta:
		model = Time
		exclude = ('id', 'meeting')
		order_by = ('participant', 'join_time')
		attrs = {"class": "table table-striped table-borderless table-sm"}
		empty_text = 'В таблице нет данных'

	def render_duration(self, value):
		return f'{value//60} минут'
