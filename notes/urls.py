from rest_framework.routers import DefaultRouter

from notes.views import UserProfileViesSet, HubViewSet, CarLoanCenterViewSet, NotesViewSet

router = DefaultRouter()

router.register(r"user_profile", UserProfileViesSet)
router.register(r"hub", HubViewSet)
router.register(r"car_loan_center", CarLoanCenterViewSet)
router.register(r"", NotesViewSet)

urlpatterns = router.urls