from django.contrib.auth.models import User
from rest_framework import serializers
from snippets.models import Snippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    highlight = serializers.HyperlinkedIdentityField(view_name="snippet-highlight", format="html")

    class Meta:
        model = Snippet
        fields = ["url", "id", "highlight", "owner", "title",
                  "code", "linenos", "language", "style"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="snippet-detail",
        read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]

    def create(self, validated_data):
        """Create and return a new `Snippet` instance, given the validated data"""
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return an existing `Snippet` instance, given the validated data"""
        instance.highlight = validated_data.get("highlight", instance.highlight)
        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save()

        return instance
