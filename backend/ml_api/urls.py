from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ml_api.views import DatasetViewSet, AlgorithmViewSet, ExperimentViewSet, CreateUserView, AlgorithmVariantViewSet

router = DefaultRouter()
router.register(r"datasets", DatasetViewSet, basename="dataset")
router.register(r"algorithms", AlgorithmViewSet, basename="algorithm")
router.register(r"algorithm-variants", AlgorithmVariantViewSet, basename="algorithm-variant")
router.register(r"experiments", ExperimentViewSet, basename="experiment")

urlpatterns = [
    path("", include(router.urls)),
    path("user/register",CreateUserView.as_view(), name="register")
]