# -*- coding: utf-8 -*-

# This file defines the entities needed by our legislation.

from openfisca_core.entities import build_entity

Familia = build_entity(
    key="familia",
    plural="families",
    label=u'Familia',
    roles=[{
            'key': 'adult',
            'plural': 'adults',
            'label': u'Adults',
            'max': 2,
            'subroles': ['primer_adult', 'segon_adult']
        },
        {
            'key': 'demandant',
            'label': u'Demandant',
            'max': 1
        },
        {
            'key': 'altre_adult',
            'plural': 'altres_adults',
            'label': u'Other adults'
        },
        {
            'key': 'menor',
            'plural': 'menors',
            'label': u'Menor',
        }]
    )

unitat_de_convivencia = build_entity(
    key="unitat_de_convivencia",
    plural="unitats_de_convivencia",
    label=u'Unitat de convivència',
    roles=[{
            'key': 'demandant',
            'label': u'Demandant',
            'max': 1
        },
        {
            'key': 'membre',
            'plural': 'membres',
            'label': u'Membres',
        }]
    )

Persona = build_entity(
    key="persona",
    plural="persones",
    label=u'Persona',
    is_person=True,
    )

entities = [Familia, unitat_de_convivencia, Persona]
