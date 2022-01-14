from rest_framework_mongoengine import serializers
from .models import NiftyFifty


class FeedSerializer(serializers.DocumentSerializer):

    class Meta:
        model = NiftyFifty
        fields = '__all__'
