from django.contrib import admin
from ml_api.models import Dataset, Algorithm, Experiment, AlgorithmVariant

admin.site.register(Dataset)
admin.site.register(Algorithm)
admin.site.register(Experiment)
admin.site.register(AlgorithmVariant)


