from rest_framework.routers import DefaultRouter

from notes.views import (
    CarLoanCenterViewSet,
    HubViewSet,
    NotesViewSet,
)

router = DefaultRouter()

router.register(r"hub", HubViewSet)
router.register(r"car-loan-center", CarLoanCenterViewSet)
router.register(r"", NotesViewSet)

urlpatterns = router.urls
