from django.core.management.base import BaseCommand


import dateutil.parser
from datetime import datetime, timezone

import requests, json

from ._config import MY_ID as myid
from ._config import JWT_TOKEN as token
from charis.models import Meeting, Participant, Time
from .synchparticipants import create_participants

today = datetime.strftime(datetime.now(), '%Y-%m-%d')

headers = {
	'authorization': f"Bearer {token}",
	'content-type': "application/json"
	}
api = 'https://api.zoom.us/v2/'


def write_json(data):
	with open('answer.json', 'w') as file:
		json.dump(data, file, indent=2, ensure_ascii=False)


def parse_iso_time(striso):
	"""
	Принимает на вход строку - время в формате 'ISO 8601'

	Возвращает объект datetime.datetime в формате местного времени
	"""

	utcdate = dateutil.parser.parse(striso)
	return utcdate.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_meetings(fr=today, to=today):
	"""
	Принимает на вход два аргумента - строки в формате '2021-01-01':
		fr - дата начала фильтра
		to - дата конца фильтра

	Возвращает словарь из зум-конференций за этот период
	"""

	methods = f'report/users/{myid}/meetings'
	qs = f'?from={fr}&to={to}'
	url = api + methods + qs

	response = requests.get(url=url, headers=headers).json()

	return response


def create_meetings(fr=today, to=today):

	response = get_meetings(fr, to)

	for meeting in response['meetings']:
		uuid = meeting['uuid']
		id = meeting['id']
		topic = meeting['topic']
		start_time = parse_iso_time(meeting['start_time'])
		end_time = parse_iso_time(meeting['end_time'])
		duration = meeting['duration']
		total_minutes = meeting['total_minutes']

		obj, created = Meeting.objects.get_or_create(
			uuid=uuid, id=id, topic=topic, start_time=start_time,
			end_time=end_time, duration=duration, total_minutes=total_minutes
			)
		print(f'obj = {obj}, created = {created}')

		create_participants(obj.uuid)


class Command(BaseCommand):
	help = 'Синхронизировать zoom-конференции с БД + участников'

	def handle(self, *args, **options):
		create_meetings(*args)


	def add_arguments(self, parser):
		parser.add_argument(nargs='*',
							type=str,
							dest = 'args',
							help='Фильтр дат: от и до')