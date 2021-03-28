# Данные

export_formats = ['csv', 'json', 'latex', 'ods', 'tsv', 'xls', 'xlsx', 'yaml']

# Остальное

class DataMixin:

	def get_user_context(self, **kwargs):
		context = kwargs
		context['export_formats'] = export_formats.copy()
		context['activeurl'] = self.request.path
		return context
