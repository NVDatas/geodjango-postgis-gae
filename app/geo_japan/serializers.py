from rest_framework import serializers

from geo_japan import models


class JapanListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Japan
        fields = (
            'jcode',
            'ken',
            'sicho',
            'gun',
            'seirei',
            'sikuchoson',
            'city_eng',
            'p_num',
            'h_num',
            'geom',
            'id',
            'url',
        )
        read_only_fields = (
            'id',
            'url',
        )
