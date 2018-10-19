from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Japan(models.Model):
    """
    全国市区町村界データ
    https://www.esrij.com/products/japan-shp/
    """

    jcode = models.CharField(
        _('市区町村コード'),
        max_length=5,
        blank=False,
        help_text=_('5 桁の JIS コード'),
    )
    ken = models.CharField(
        _('都道府県名'),
        max_length=10,
        blank=False,
        help_text=_(''),
    )
    sicho = models.CharField(
        _('支庁名・振興局名'),
        max_length=20,
        blank=True,
        help_text=_(''),
    )
    gun = models.CharField(
        _('郡名（町村部のみ）'),
        max_length=20,
        blank=True,
        help_text=_(''),
    )
    seirei = models.CharField(
        _('政令指定都市の市名'),
        max_length=20,
        blank=True,
        help_text=_(''),
    )
    sikuchoson = models.CharField(
        _('市区町村名'),
        max_length=50,
        blank=True,
        help_text=_('政令指定都市の場合は区名'),
    )
    city_eng = models.CharField(
        _('市区町村名（英語）'),
        max_length=50,
        blank=False,
        help_text=_(''),
    )
    p_num = models.IntegerField(
        _('人口'),
        null=True,
        help_text=_('「住民基本台帳に基づく人口、人口動態及び世帯数（平成 28 年 1 月 1 日現在） 総務省」による'),
    )
    h_num = models.IntegerField(
        _('世帯数'),
        null=True,
        help_text=_('「住民基本台帳に基づく人口、人口動態及び世帯数（平成 28 年 1 月 1 日現在） 総務省」による'),
    )
    geom = models.MultiPolygonField(
        srid=4612,
        null=False,
        help_text=_('content - points フィールドの geojson - Point 表現'),
    )

    class Meta:
        indexes = (
            models.Index(fields=['jcode', ]),
        )

    def __str__(self):
        return f'{self.jcode}'
