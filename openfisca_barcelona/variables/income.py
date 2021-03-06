# -*- coding: utf-8 -*-

# This file defines the variables of our legislation.
# A variable is property of a person, or an entity (e.g. a familia).
# See https://doc.openfisca.fr/variables.html

# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *


class ingressos_bruts(Variable):
    column = FloatCol
    entity = Persona
    definition_period = MONTH
    label = "Actual amount available to the person at the end of the month"
    set_input = set_input_divide_by_period

    def formula(persona, period):
        return persona("salari_net", period)


class familia_ingressos_bruts(Variable):
    column = IntCol(val_type="monetary")
    entity = Familia
    definition_period = MONTH
    label = "Total yearly income"
    set_input = set_input_divide_by_period

    def formula(familia, period):
        ingressos_membres_de_la_familia = familia.members('ingressos_bruts', period)
        total_ingressos_familia = familia.sum(ingressos_membres_de_la_familia)
        return total_ingressos_familia


class salari_net(Variable):
    column = FloatCol
    entity = Persona
    definition_period = MONTH
    label = "Amount the person is earning due her work"
    set_input = set_input_divide_by_period
