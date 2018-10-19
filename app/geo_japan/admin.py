from django.contrib.gis import admin

from geo_japan import models


@admin.register(models.Japan)
class JapanAdmin(admin.OSMGeoAdmin):
    list_display = ('jcode', 'ken', 'sikuchoson', 'p_num',)
    ordering = ('jcode',)

    map_srid = 3857
    display_srid = True
    units = 'm'
