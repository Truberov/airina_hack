from rest_framework.routers import DefaultRouter

from docs.viewsets import (
    ArchiveViewSet,
)

router = DefaultRouter()
router.register(
    'archives',
    ArchiveViewSet,
    basename='docs'
)

urlpatterns = router.urls
