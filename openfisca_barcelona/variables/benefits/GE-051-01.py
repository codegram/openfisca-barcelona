# Import from openfisca-core the common python objects used to code the legislation in OpenFisca
from openfisca_core.model_api import *
# Import the entities specifically defined for this tax and benefit system
from openfisca_barcelona.entities import *

class grau_discapacitat(Variable):
    column = IntCol
    entity = Persona
    definition_period = MONTH
    label = "User's grade of disability"
    set_input = set_input_dispatch_by_period
    default = False


class ha_esgotat_prestacio_de_desocupacio(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user is not receiving any benefit for not having a job"
    set_input = set_input_dispatch_by_period
    default = False


class demandant_d_ocupacio_durant_12_mesos(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has been searching for a job at least 12 months"
    set_input = set_input_dispatch_by_period
    default = False


class durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "During the previous month the user has applied for a job"
    set_input = set_input_dispatch_by_period
    default = False


class beneficiari_ajuts_per_violencia_de_genere(Variable):
    column = BoolCol
    entity = Persona
    definition_period = MONTH
    label = "The user has a violence of genre  benefit"
    set_input = set_input_dispatch_by_period
    default = False


class GE_051_01_mensual(Variable):
    column = IntCol(val_type="monetary")
    entity = Persona
    definition_period = MONTH
    label = "GE_051_1 - RAI 1 - Ajuda discapacitats 33% o superior"

    def formula(persona, period, parameters):
        cap_membre_amb_ingressos_superiors_a_530_mensuals = \
            persona.familia('cap_familiar_te_renda_disponible_superior_a_530', period)
        discapacitat_superior_al_33_percent = persona('grau_discapacitat', period) > 33
        ha_esgotat_prestacio_de_desocupacio = persona('ha_esgotat_prestacio_de_desocupacio', period)
        demandant_d_ocupacio_durant_12_mesos = persona('demandant_d_ocupacio_durant_12_mesos', period)
        durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina = \
            persona('durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina', period)
        no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos = \
            persona('no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos', period)
        no_se_li_ha_concedit_tres_ajudes_rai_anteriors = persona('no_se_li_ha_concedit_tres_ajudes_rai_anteriors', period)
        no_treballa_per_compte_propi = persona('treballa_per_compte_propi', period) == False
        no_ingressat_en_centre_penitenciari = persona('ingressat_en_centre_penitenciari', period) == False
        no_percep_prestacins_incompatibles_amb_la_feina = \
            persona('percep_prestacions_incompatibles_amb_la_feina', period) == False
        no_beneficiari_ajuts_per_violencia_de_genere = \
            persona('beneficiari_ajuts_per_violencia_de_genere', period) == False

        compleix_els_requeriments = \
            cap_membre_amb_ingressos_superiors_a_530_mensuals \
            * discapacitat_superior_al_33_percent \
            * ha_esgotat_prestacio_de_desocupacio \
            * demandant_d_ocupacio_durant_12_mesos \
            * durant_el_mes_anterior_ha_presentat_solicituds_recerca_de_feina \
            * no_se_li_ha_concedit_cap_ajuda_rai_en_els_ultims_12_mesos \
            * no_se_li_ha_concedit_tres_ajudes_rai_anteriors \
            * no_treballa_per_compte_propi \
            * no_ingressat_en_centre_penitenciari \
            * no_percep_prestacins_incompatibles_amb_la_feina \
            * no_beneficiari_ajuts_per_violencia_de_genere

        import_ajuda = parameters(period).benefits.GE051.import_ajuda
        return where(compleix_els_requeriments, import_ajuda, 0)
