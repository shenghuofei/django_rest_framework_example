from rest_framework import serializers
from restapp.models import Snippet,LANGUAGE_CHOICES, STYLE_CHOICES
class spsl(serializers.ModelSerializer):
    class Meta:
        #owner = serializers.ReadOnlyField(source='owner.username')
        model = Snippet
        fields = ('id','title','code','linenos','language','style','owner','highlighted')
        #fields = ('id','title','code','linenos')
