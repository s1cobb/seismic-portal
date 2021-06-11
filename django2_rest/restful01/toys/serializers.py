from toys.models import Toys
from rest_framework import serializers

class ToySerializer(serializers.ModelSerializer):
    class Meta:
        model = Toys
        fields = ('pk', 'name', 'description', 'release_date',
                  'toy_category', 'was_included_in_home')
