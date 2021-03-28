from django.core.management.base import BaseCommand


import dateutil.parser
from datetime import datetime, timezone

import requests, json

from ._config import MY_ID as myid
from ._config import JWT_TOKEN as token
from charis.models import Meeting, Participant, Time

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

def get_participants(uuid_of_meeting):
	"""Принимает на вход id конференции, возвращает список участников"""

	methods = f'report/meetings/{uuid_of_meeting}/participants'
	url = api + methods

	response = requests.get(url=url, headers=headers).json()
	write_json(response)
	return response


def create_participants(uuid_of_meeting):

	response = get_participants(uuid_of_meeting)

	for participant in response['participants']:
		id = participant['user_id']
		name = participant['name']
		user_email = participant['user_email']
		join_time = parse_iso_time(participant['join_time'])
		leave_time = parse_iso_time(participant['leave_time'])
		duration = participant['duration']

		try:
			obj, created = Participant.objects.get_or_create(
			id=id, name=name, user_email=user_email
			)
			print(f'Participant: {obj} создан?: {created}')
		except Exception as e:
			print(repr(e))

		obj, created = Time.objects.get_or_create(
			meeting = Meeting.objects.get(uuid=uuid_of_meeting),
			participant = Participant.objects.get(id=id),
			join_time = join_time,
			leave_time = leave_time,
			duration = duration
			)

		print(f'Time: obj = {obj}, created = {created}')



class Command(BaseCommand):
	help = 'Синхронизировать участников zoom-конференций с БД'

	def handle(self, *args, **options):
		create_participants(args[0])


	def add_arguments(self, parser):
		parser.add_argument(nargs='+',
							type=str,
							dest = 'args',
							help='UUID конференции')