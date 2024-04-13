from django.db.models import Q
from rest_framework import viewsets, mixins, permissions as drf_permissions, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from docs.models import DocumentsArchive
from docs.serializers import (
    DocumentsArchiveSerializer, DocumentsArchivePostSerializer
)


class ArchiveViewSet(
    viewsets.ModelViewSet
):
    permission_classes = ()
    serializer_class_map = {
        'list': DocumentsArchiveSerializer,
        'retrieve': DocumentsArchiveSerializer,
        'create': DocumentsArchivePostSerializer,
    }
    queryset = DocumentsArchive.objects.all()
    # filterset_class = PromptProductFilterSet
    # search_fields = ('name', 'description',)

    def get_serializer_class(self):
        return self.serializer_class_map.get(self.action, DocumentsArchiveSerializer)

    # @action(detail=True, methods=['POST'], url_path='upload_document', parser_classes=(MultiPartParser, FormParser))
    # def upload_file(self, request, id=None):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(prompt_product=instance.data)
#
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
