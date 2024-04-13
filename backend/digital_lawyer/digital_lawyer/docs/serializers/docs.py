from rest_framework import serializers

from docs.models import Document, DocumentsArchive


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('id', 'created_at', 'updated_at')

    def to_representation(self, instance):  # TODO: Переписать эту хуйню!
        """
        Обрезает урл от лишней инфы
        """
        ret = super().to_representation(instance)
        ret['file'] = ret['file'].split('?')[0]
        return ret


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        exclude = ('created_at', 'id', 'updated_at', 'docs_group',)

class DocumentsArchiveSerializer(serializers.ModelSerializer):
    docs = DocumentSerializer(many=True, read_only=True)
    class Meta:
        model = DocumentsArchive
        exclude = ('created_at', 'id', 'updated_at')


class DocumentsArchivePostSerializer(DocumentsArchiveSerializer):
    docs = serializers.ListField(child=serializers.FileField(), write_only=True)
    docs_classes = serializers.ListField(child=serializers.CharField(), write_only=True)

    def create(self, validated_data):
        docs_data = validated_data.pop('docs')
        docs_classes = validated_data.pop('docs_classes')

        instance = DocumentsArchive.objects.create(**validated_data)

        for i, doc in enumerate(docs_data):
            Document.objects.create(file=doc, predicted_class=docs_classes[i], docs_group=instance)

        return instance
