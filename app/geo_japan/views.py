from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, IsoDateTimeFilter, CharFilter
from rest_framework import viewsets, mixins, permissions

from geo_japan import models
from geo_japan import serializers


class JapanListFilterSet(FilterSet):
    jcode_description = _('市区町村コード')
    jcode = CharFilter(
        label=jcode_description,
        help_text=jcode_description,
        field_name='jcode',
        lookup_expr='exact',
    )

    class Meta:
        model = models.Japan
        fields = ()


class JapanList(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    list:
    全国市区町村界データ一覧の取得
    """

    permission_classes = (permissions.AllowAny,)

    serializer_class = serializers.JapanListSerializer

    filter_backends = (DjangoFilterBackend,)

    filterset_class = JapanListFilterSet

    ordering_fields = ('modified',)
    ordering_description = _('順序: { "modified": 更新日時(昇順), "-modified": 更新日時(降順))')

    queryset = models.Japan.objects.all()


class JapanDetail(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    retrieve:
    全国市区町村界データ詳細の取得
    """

    permission_classes = (permissions.AllowAny,)

    serializer_class = serializers.JapanListSerializer

    queryset = models.Japan.objects.all()
