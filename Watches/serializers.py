from rest_framework import serializers
from .models import *
from rest_framework.exceptions import ValidationError
from User.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'



# при ListAPIView нужен ModelSerializer
class WatchSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Watch
        fields = 'id title description price category'.split()

        def get_photos(self, watch):
            return watch.get_photos_list()


class WatchValidateSerializers(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    price = serializers.IntegerField()
    category = serializers.ListField(required=True)
    photo = serializers.ListField(required=True)

    class Meta:
        model = Watch
        fields = 'id title description price category'.split()

    def validate_title(self, title):
        try:
            Watch.objects.get(id=title)
        except Watch.DoesNotExist:
            raise ValidationError('Title does not exists!')
        return title

    def validate_category(self, category):
        if len(category) == Category.objects.filter(id__in=category).count():
            return category
        raise ValidationError("some of given categories does not exists")

    def validate_photo(self, photo):
        if len(photo) == Photo.objects.filter(id__in=photo).count():
            return photo
        raise ValidationError("some of given photos does not exists")



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewValidateSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(min_value=1)
    title = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=255)
    stars = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        model = Review
        fields = 'author_id title text stars'.split()

    def validate_author_id(self, author_id):
        author_exists = User.objects.filter(id=author_id).exists()
        if author_exists:
            return author_id
        raise ValidationError('Author does not exists')


class PhotoSerializer(serializers.ModelSerializer):
    watch_id = serializers.IntegerField(min_value=1)

    class Meta:
        model = Photo
        fields = 'watch_id image'.split()

    def validate_watch_id(self, watch_id):
        watch_exists = Watch.objects.filter(id=watch_id).exists()
        if watch_exists:
            return watch_id
        raise ValidationError('watchs does not exists')

