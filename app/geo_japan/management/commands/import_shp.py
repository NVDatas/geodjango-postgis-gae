from logging import getLogger

import os
import argparse
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from django.db import transaction

from geo_japan.models import Japan

logger = getLogger(__name__)


class Command(BaseCommand):
    help = "Importing Spatial Data (LayerMapping)"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            '-I',
            '--shp_url',
            nargs=1,
            required=True,
            type=str,
            help='import shp URL'
        )

    @transaction.non_atomic_requests
    def handle(self, *args, **options):
        logger.info(f'{os.path.basename(__file__)}. start.')

        border_shp: str = options['shp_url'][0]
        border_mapping = {
            'jcode': 'JCODE',
            'ken': 'KEN',
            'sicho': 'SICHO',
            'gun': 'GUN',
            'seirei': 'SEIREI',
            'sikuchoson': 'SIKUCHOSON',
            'city_eng': 'CITY_ENG',
            'p_num': 'P_NUM',
            'h_num': 'H_NUM',
            'geom': 'MULTIPOLYGON',
        }
        lm = LayerMapping(Japan, border_shp, border_mapping, transform=False, encoding='utf8')
        lm.save(strict=True, verbose=False)
        logger.info(f'{os.path.basename(__file__)}. end.')
