from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ml_api.views import DatasetViewSet, AlgorithmViewSet, ExperimentViewSet

router = DefaultRouter()
router.register(r"datasets", DatasetViewSet, basename="dataset")
router.register(r"algorithms", AlgorithmViewSet, basename="algorithm")
router.register(r"experiments", ExperimentViewSet, basename="experiment")

urlpatterns = [
    # Expose all viewsets under /api/ within the project-level URL config.
    path("", include(router.urls)),
]