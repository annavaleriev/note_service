from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.urls import path

from notes.views import UserProfileViesSet, HubViewSet, CarLoanCenterViewSet, NotesViewSet

router = DefaultRouter()

router.register(r"user_profile", UserProfileViesSet)
router.register(r"hub", HubViewSet)
router.register(r"car_loan_center", CarLoanCenterViewSet)
router.register(r"notes", NotesViewSet)


urlpatterns = [
    # path("admin/", admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs")
]
