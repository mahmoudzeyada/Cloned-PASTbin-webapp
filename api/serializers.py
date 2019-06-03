from django.utils.timesince import timesince
from django.contrib.auth import get_user_model


from rest_framework import serializers

from .models import Document, SharedDocuments

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    '''serializer for user '''
    class Meta:
        model = User
        fields = ("id", "username")


class DocumentSerializer(serializers.ModelSerializer):
    ''' Serializer for Document  '''
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    users_to_share_with = serializers.MultipleChoiceField(
        [user.username for user in User.objects.all()],
        allow_null=True
    )
    document_shared_with = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")

    def get_time_since(self, obj):
        return timesince(obj.created_at)

    def get_document_shared_with(self, obj):
        qs = SharedDocuments.objects.filter(document=obj)
        if qs:
            return ([{"id": doc.users.id,
                      "username": doc.users.username} for doc in qs])

        return None

    def create(self, validated_data):
        users_to_share_with = validated_data.pop("users_to_share_with")
        # insuring that there is a user or not
        if self.context["request"].user.id:
            validated_data["owner"] = self.context["request"].user

        document = super().create(validated_data)
        # insuring that we can put it in SharedDocuments table
        if self.context["request"].user.id:
            SharedDocuments.objects.create(
                users=self.context["request"].user, document=document)
        # looping through the list to save doc to shared users
        if users_to_share_with:
            for username in users_to_share_with:
                user = User.objects.get(username=username)
                SharedDocuments.objects.create(users=user, document=document)

        return document

    def update(self, instance, validated_data):

        if "users_to_share_with" in validated_data:
            users_to_share_with = validated_data.get("users_to_share_with")
            qs = SharedDocuments.objects.filter(document=instance)
            # excluding the document's user from qs
            qs = qs.exclude(users=self.context["request"].user)
            # deleteing all entries for that user
            qs.delete()
            # looping through the list to save doc to shared users
            if users_to_share_with:
                for username in users_to_share_with:
                    user = User.objects.get(username=username)
                    SharedDocuments.objects.create(users=user,
                                                   document=instance)
            return instance

        return super().update(instance, validated_data)


class SharedDocumentsSerializer(serializers.ModelSerializer):
    ''' serializer for shared Documents '''
    users = UserSerializer(many=False, read_only=True)
    document = DocumentSerializer(many=False, read_only=True)

    class Meta:
        model = SharedDocuments
        fields = "__all__"
