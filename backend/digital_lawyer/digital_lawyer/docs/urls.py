from rest_framework.routers import DefaultRouter

from docs.viewsets import (
    ArchiveViewSet, DocumentViewSet
)

router = DefaultRouter()
router.register(
    'archives',
    ArchiveViewSet,
    basename='archives'
)

router.register(
    'documents',
    DocumentViewSet,
    basename='documents'
)


urlpatterns = router.urls
