# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from datetime import datetime
from openfisca_barcelona.variables.demographics import *

class resident_a_catalunya_durant_5_anys(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has legal residence in catalonia for at least 5 years"
    set_input = set_input_dispatch_by_period
    default = False


class victima_de_terrorisme(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is a victim of terrorism"
    set_input = set_input_dispatch_by_period
    default = False


class ingressos_suficients_per_pagar_el_lloguer(Variable):
    column = BoolCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "The familia income is enough to pay rent"
    set_input = set_input_dispatch_by_period
    default = False


class risc_d_exclusio_social(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is in risk of social exclusion"
    set_input = set_input_dispatch_by_period

    def formula(unitat_de_convivencia, period, legislation):
        return unitat_de_convivencia("nivell_de_risc_d_exclusio_social", period) != NIVELL_DE_RISC_D_EXCLUSIO_SOCIAL["No"]


class existeix_un_contracte_de_lloguer(Variable):
    column = BoolCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "The user has a rent contract"
    set_input = set_input_dispatch_by_period
    default = False


class LLOGMAXBCN(Variable):     # Fixme: This should be in parameters
    column = BoolCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "The house hold rent does not exceed maximum rent amount for Barcelona"
    set_input = set_input_dispatch_by_period
    default = False


class esta_al_corrent_del_pagament_de_lloguer(Variable):
    column = BoolCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "The rent payments must be up to date"
    set_input = set_input_dispatch_by_period
    default = False


class lloguer_domiciliat(Variable):
    column = BoolCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "The rent payments are made through a bank"
    set_input = set_input_dispatch_by_period
    default = False


class pot_rebre_subvencions(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is not subject to any condition that is forbidden"
    set_input = set_input_dispatch_by_period
    default = False


class al_corrent_de_les_obligacions_tributaries(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is up to date with her obligations against the state"
    set_input = set_input_dispatch_by_period
    default = False


class es_BLJ(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has more than 65 years at 31/12/2012"
    set_input = set_input_dispatch_by_period

    def formula(persona, period, legislation):
        return major_de_65_el_2012_12_31(persona('data_naixement',period))


def major_de_65_el_2012_12_31(data_de_naixement):
    return data_de_naixement < datetime.strptime('1948-1-1', "%Y-%m-%d").date()


class import_del_lloguer(Variable):
    column = FloatCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "Rent amount payed every month"
    set_input = set_input_dispatch_by_period


class HG_077_mensual(Variable):
    column = FloatCol
    entity = unitat_de_convivencia
    definition_period = MONTH
    label = "AJUT PER AL PAGAMENT DEL LLOGUER"
    set_input = set_input_dispatch_by_period

    def formula(unitat_de_convivencia, period, parameters):
        compleix_els_requeriments = \
            ((unitat_de_convivencia('ingressos_suficients_per_pagar_el_lloguer', period)
              + unitat_de_convivencia.demandant('victima_de_terrorisme', period)) > 0) \
            * unitat_de_convivencia('LLOGMAXBCN', period) \
            * unitat_de_convivencia('esta_al_corrent_del_pagament_de_lloguer', period) \
            * unitat_de_convivencia('lloguer_domiciliat', period) \
            * unitat_de_convivencia.demandant('resident_a_catalunya_durant_5_anys', period) \
            * unitat_de_convivencia.demandant('risc_d_exclusio_social', period) \
            * unitat_de_convivencia('existeix_un_contracte_de_lloguer', period) \
            * unitat_de_convivencia.demandant('pot_rebre_subvencions', period) \
            * unitat_de_convivencia.demandant('al_corrent_de_les_obligacions_tributaries', period)
        irsc = parameters(period).benefits.HG077.IRSC
        irsc_per_0_94 = irsc * 0.94
        lloguer_just = where(unitat_de_convivencia.demandant('ingressos_disponibles', period)/12 > irsc_per_0_94,
                             unitat_de_convivencia.demandant('ingressos_disponibles', period)/12 * 0.3,
                             unitat_de_convivencia.demandant('ingressos_disponibles', period)/12 * 0.2)
        import_ajuda_maxim_pels_BLJ = parameters(period).benefits.HG077.BLJ_ajuda_maxima_anual/12
        import_ajuda_maxim_pels_no_BLJ = parameters(period).benefits.HG077.no_BLJ_ajuda_maxima_anual / 12
        import_ajuda_minim_pels_no_BLJ = parameters(period).benefits.HG077.no_BLJ_ajuda_minima_anual / 12
        import_ajuda_BLJ = max_(
            min_(unitat_de_convivencia('import_del_lloguer', period) - lloguer_just, import_ajuda_maxim_pels_BLJ), 0)
        import_ajuda_no_BLJ = \
            max_(
                min_(
                    unitat_de_convivencia('import_del_lloguer', period)
                    - lloguer_just, import_ajuda_maxim_pels_no_BLJ),
                import_ajuda_minim_pels_no_BLJ)
        estat_BLJ = unitat_de_convivencia.members('es_BLJ', period)
        existeix_algun_BLJ = unitat_de_convivencia.any(estat_BLJ)
        import_ajuda = where(existeix_algun_BLJ, import_ajuda_BLJ, import_ajuda_no_BLJ)

        return where(compleix_els_requeriments, import_ajuda, 0)
