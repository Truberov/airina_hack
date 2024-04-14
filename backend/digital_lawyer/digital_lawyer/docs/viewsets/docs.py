from rest_framework import viewsets, mixins, status

from docs.models import DocumentsArchive, Document
from docs.serializers import (
    DocumentsArchiveSerializer, DocumentsArchivePostSerializer, DocumentSerializer
)


class ArchiveViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,

):
    permission_classes = ()
    serializer_class_map = {
        'list': DocumentsArchiveSerializer,
        'retrieve': DocumentsArchiveSerializer,
        'create': DocumentsArchivePostSerializer,
    }
    queryset = DocumentsArchive.objects.order_by('-created_at')
    search_fields = ('name',)

    def get_serializer_class(self):
        return self.serializer_class_map.get(self.action, DocumentsArchiveSerializer)


class DocumentViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = ()
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    search_fields = ('filename',)
    filterset_fields = ('predicted_class',)
