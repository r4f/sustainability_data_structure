"""
TODO: check with Django DB that exporting to the webpage works
without unnecessary restructuring and renaming.
"""

import pandas as pd
from enum import Enum
import mongoengine


class ESG(mongoengine.EmbeddedDocument):
    """ESG Assessment Data

    Overall score (/100):
    >60: Advanced
    50-59: Robust
    30-49: Limited
    0-29: Weak
    """
    ESG = mongoengine.IntField() # ESG Overall score
    E = mongoengine.IntField() # Environment Pillar score
    S = mongoengine.IntField() # Social Pillar score
    G = mongoengine.IntField() # Governance Pillar score


class PAIFloatIndicator(mongoengine.EmbeddedDocument):
    indicator = mongoengine.FloatField()
    reporting_year = mongoengine.StringField()

class PAIBooleanIndicator(mongoengine.EmbeddedDocument):
    indicator = mongoengine.BooleanField()
    reporting_year = mongoengine.StringField()

class PAI1(mongoengine.EmbeddedDocument):
    #1. Scope 1 Emissions (Metric Tons of CO2 equivalent)
    scope1 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #1. Scope 2 Emissions (Metric Tons of CO2 equivalent)
    scope2 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #1. Scope 3 GHG emissions (from 1 January 2023) (Metric Tons of CO2 equivalent)
    scope3 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #1. Total GHG emissions
    total = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)

class PAI5(mongoengine.EmbeddedDocument):
    """Share of non-renewable energy consumption and production."""
    #5. Non-renewable energy consumption/Total energy consumption
    consumption = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #5. Non-renewable energy production/Total energy production
    production = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)

class PAI(mongoengine.EmbeddedDocument):
    """PAI as reported in SFDR.

    PAI 15-18 are also defined, but not used in our dataset.
    """

    PAI01 = mongoengine.EmbeddedDocumentField(PAI1)
    #2. Carbon footprint (as defined by SFDR)
    PAI02 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #3. GHG intensity of investee companies
    PAI03 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #4. Exposure to companies active in the fossil fuel sector
    PAI04 = mongoengine.EmbeddedDocumentField(PAIBooleanIndicator)

    #5: Share of non-renewable energy consumption and production."""
    PAI05 = mongoengine.EmbeddedDocumentField(PAI5)
    # PAI 6: Energy consumption intensity per high impact climate sector
    PAI06 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #7. Activities negatively affecting biodiversity - sensitive areas - PROXY
    PAI07 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #8. Emissions to water
    PAI08 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #9. Hazardous Waste (Tonnes)
    PAI09 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #10. Violations of UNGC principles and OECD
    PAI10 = mongoengine.EmbeddedDocumentField(PAIBooleanIndicator)
    #11. Lack of processes and compliance mechanisms to monitor compliance with UNGC principles and OECD
    PAI11 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #12. Unadjusted Gender Pay Gap Average
    PAI12 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #13. Board gender diversity
    PAI13 = mongoengine.EmbeddedDocumentField(PAIFloatIndicator)
    #14. Exposure to controversial weapons
    PAI14 = mongoengine.EmbeddedDocumentField(PAIBooleanIndicator)

    additional_indicators = mongoengine.DictField()

    @classmethod
    def from_dict(cls, data: dict | pd.Series):
        """create PAI object from a dictionary

        :param data: dict such as
            {
                "PAI01.scope1.indicator": 0.1234,
                "PAI01.scope1.reporting_year": 2012,
                "PAI01.scope2.indicator": 0.1234,
                "PAI01.scope2.reporting_year": 2012,
                "PAI03.indicator": 0.1234,
                "PAI03.reporting_year": 2012,
                "PAI10.indicator": False,
                "PAI10.reporting_year": 2022,
            }
        :return: PAI object
        """
        pass

class EU_taxonomy(mongoengine.EmbeddedDocument):
    """EU taxonomy"""
    eligible = mongoengine.BooleanField()
    #aligned = ?

class CAS_ALC1(mongoengine.EmbeddedDocument):
    """Alcohol"""
    c_2 = mongoengine.FloatField() # Production of alcoholic beverages

class CAS_ANIM1(mongoengine.EmbeddedDocument):
    """Animal Welfare"""
    c_1_1 = mongoengine.FloatField() # Production of cosmetic products tested on animals
    c_2_1 = mongoengine.FloatField() # Production of non-cosmetic products tested on animals - Manufacturers
    c_2_2 = mongoengine.FloatField() # Production of non-cosmetic products tested on animals - Distributors
    c_4 = mongoengine.BooleanField() # irresponsible animal testing for medical purpose
    c_5 = mongoengine.FloatField() # Production and sale of fur products
    c_6 = mongoengine.FloatField() # Intensive farming operations

class CAS_CHEM1(mongoengine.EmbeddedDocument):
    """Chemicals of Concern"""
    c_1 = mongoengine.FloatField() # Production of restricted chemicals
    c_3_1 = mongoengine.FloatField() # Production of pesticides - Manufacturers

class CAS_CFA1(mongoengine.EmbeddedDocument):
    """Civilian Firearms"""
    c_1 = mongoengine.FloatField() # Production or sale of civilian firearms

class CAS_FOSF2(mongoengine.EmbeddedDocument):
    """Coal"""
    c_2_3 = mongoengine.FloatField() # Thermal coal mining
    c_2_4 = mongoengine.FloatField() # Coal-fuelled power generation

class CAS_FOSF1(mongoengine.EmbeddedDocument):
    """Fossil Fuels Industry"""
    c_1_1 = mongoengine.FloatField() # Fossil fuels industry - Upstream
    c_1_2 = mongoengine.FloatField() # Fossil fuels industry - Midstream


class CAS_GAMB1(mongoengine.EmbeddedDocument):
    """Gambling"""
    c_1 = mongoengine.FloatField() # Gambling operations or products

class CAS_MIL1(mongoengine.EmbeddedDocument):
    """Military"""
    c_1 = mongoengine.FloatField() # Military sales
    c_2 = mongoengine.FloatField() # Controversial weapons
    c_3 = mongoengine.FloatField() # Financing of cluster munitions or anti-personnel landmines

class CAS_NUCL1(mongoengine.EmbeddedDocument):
    """Nuclear Power"""
    c_1_1 = mongoengine.FloatField() # Turnover from nuclear power
    c_1_5 = mongoengine.FloatField() # Uranium mining

class CAS_PORN1(mongoengine.EmbeddedDocument):
    """Pornography"""
    c_2 = mongoengine.FloatField() # Pornography and adult entertainment services

class CAS_FOSF3(mongoengine.EmbeddedDocument):
    """Unconventional Oil and Gas Involvement"""
    c_1 = mongoengine.FloatField() # Tar sands and oil shale extraction or services
    c_4_1 = mongoengine.FloatField() # Offshore arctic drilling
    c_4_5 = mongoengine.FloatField() # Hydraulic fracturing

class CAS_TOB1(mongoengine.EmbeddedDocument):
    """Tobacco"""
    c_2 = mongoengine.FloatField() # Production of tobacco
    c_4 = mongoengine.FloatField() # Production of e-cigarettes

class CAS_CANN1(mongoengine.EmbeddedDocument):
    """Cannabis"""
    c_2 = mongoengine.FloatField() # Production of cannabis

class CAS_GMO1(mongoengine.EmbeddedDocument):
    """Genetic Engineering"""
    c_2 = mongoengine.BooleanField() # Production of GMOs for human consumption

class HESC1Choice(Enum):
    NO = 0
    OPEN = 1
    YES = 2

class CAS_HESC1(mongoengine.EmbeddedDocument):
    """Human Embryonic Stem Cells"""
    c_1 = mongoengine.IntField(choices=HESC1Choice) # Research on human embryonic stem cells

class CAS(mongoengine.EmbeddedDocument):
    ALC1 = mongoengine.EmbeddedDocumentField(CAS_ALC1)
    ANIM1 = mongoengine.EmbeddedDocumentField(CAS_ANIM1)
    CHEM1 = mongoengine.EmbeddedDocumentField(CAS_CHEM1)
    CFA1 = mongoengine.EmbeddedDocumentField(CAS_CFA1)
    FOSF1 = mongoengine.EmbeddedDocumentField(CAS_FOSF1)
    FOSF2 = mongoengine.EmbeddedDocumentField(CAS_FOSF2)
    FOSF3 = mongoengine.EmbeddedDocumentField(CAS_FOSF3)
    GAMB1 = mongoengine.EmbeddedDocumentField(CAS_GAMB1)
    MIL1 = mongoengine.EmbeddedDocumentField(CAS_MIL1)
    NUCL1 = mongoengine.EmbeddedDocumentField(CAS_NUCL1)
    PORN1 = mongoengine.EmbeddedDocumentField(CAS_PORN1)
    TOB1 = mongoengine.EmbeddedDocumentField(CAS_TOB1)
    CANN1 = mongoengine.EmbeddedDocumentField(CAS_CANN1)
    GMO1 = mongoengine.EmbeddedDocumentField(CAS_GMO1)
    HESC1 = mongoengine.EmbeddedDocumentField(CAS_HESC1)

class CRAChoice(Enum):
    NO_INDICATION = 0
    HIGH = 1
    SIGNIFICANT = 2
    CRITICAL = 3
class CRAItem(mongoengine.EmbeddedDocument):
    # Negative criterium
    # acceptable if below defined threshold.
    # imug rating: Literal[None, "High", "Significant", "Critical"]

    severity = mongoengine.StringField(choices = ("High", "Significant", "Critical"))
    # Rating by IMUG
    # use 0/1/2/3?

    incorporation_scale = mongoengine.FloatField()

    def is_acceptable(self):
        if self.severity != "Critical":
            return True
        else:
            return False

class CRA_ENV(mongoengine.EmbeddedDocument):
    """Environment

    NO_INDICATION = 0
    HIGH = 1
    SIGNIFICANT = 2
    CRITICAL = 3
    """
    ENV = mongoengine.IntField()

class CRA_HRT(mongoengine.EmbeddedDocument):
    """Human and Labour Rights

    NO_INDICATION = 0
    HIGH = 1
    SIGNIFICANT = 2
    CRITICAL = 3
    """

    # Fundamental human rights
    c_1_1 = mongoengine.IntField()
    # Fundamental labour rights
    c_2_1 = mongoengine.IntField()
    #No discrimination
    c_2_4 = mongoengine.IntField()
    # Child and forced labour
    c_2_5 = mongoengine.IntField()

class CRA_CS(mongoengine.EmbeddedDocument):
    """Business Behaviour

    NO_INDICATION = 0
    HIGH = 1
    SIGNIFICANT = 2
    CRITICAL = 3
    """

    #Environmental Standards in the Supply Chain 
    c_2_3 = mongoengine.IntField()
    #Social Standards in the Supply Chain
    c_2_4 = mongoengine.IntField()
    #Corruption
    c_3_1 = mongoengine.IntField()

class CRA(mongoengine.EmbeddedDocument):
    """Controversy Risk Assessment

    Incident Risk Assessment (UN Global Compact Compliance)

    Environment
    ENV         Environment
    Human and Labour Rights
    HRT 1.1		Fundamental Human rights					
	HRT 2.1		Fundamental Labour Rights					
	HRT 2.4		Non-Discrimination					
	HRT 2.5		Child and Forced Labour					
    Business Behaviour
    C&S 2.3		Environmental Standards in the Supply Chain					
	C&S 2.4		Social Standards in the Supply Chain					
	C&S 3.1		Corruption					

    """
    # Environment
    ENV = mongoengine.EmbeddedDocumentField(CRA_ENV)
    # Fundamental human rights
    HRT = mongoengine.EmbeddedDocumentField(CRA_HRT)
    CS = mongoengine.EmbeddedDocumentField(CRA_CS)

    def is_acceptable(self):
        acceptable_values = ["High", "Significant", None]
        unacceptable_values = ["Critical"]
        return True

class IntervalIndicator(mongoengine.EmbeddedDocument):
    """
    (0, 0) means "0"
    (0, 0.1) means "]0 - 10%["
    """
    lower = mongoengine.FloatField()
    mean = mongoengine.FloatField()
    upper = mongoengine.FloatField()

class ImpactThemes(mongoengine.EmbeddedDocument):
    """
    imug_rating_Goldmarie_ESG_Datenfeed_10_2023.xlsx
    "Sustainable Goods & Services Data"
    "Sustainable Product/service(s)" in the database refers to a list of concretizations of impact
    themes.
    """

    # Access to information
    access_to_information = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Capacity building
    capacity_building = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Energy & climate change (Scale of Incorporation)
    energy_and_climate_change = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Food & nutrition (Scale of Incorporation)
    food_and_nutrition = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Health (Scale of Incorporation)
    health = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Infrastructure (Scale of Incorporation)
    infrastructure = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Responsible finance (Scale of Incorporation)
    responsible_finance = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Water & sanitation (Scale of Incorporation)
    water_and_sanitation = mongoengine.EmbeddedDocumentField(IntervalIndicator)
    # Protection of ecosystems (Scale of Incorporation)
    protection_of_ecosystems = mongoengine.EmbeddedDocumentField(IntervalIndicator)

class SustainabilityReporting(mongoengine.Document):
    """New version of ESGData."""
    isin = mongoengine.StringField(required=True)
    # date of data delivery.
    date = mongoengine.DateField(required=True, unique_with="isin")

    ESG = mongoengine.EmbeddedDocumentField(ESG)
    EU_taxonomy = mongoengine.EmbeddedDocumentField(EU_taxonomy)
    CAS = mongoengine.EmbeddedDocumentField(CAS)
    CRA = mongoengine.EmbeddedDocumentField(CRA)
    PAI = mongoengine.EmbeddedDocumentField(PAI)

    # Scale of Incorporation. Overall impact score.
    sdg_involvement = mongoengine.EmbeddedDocumentField(IntervalIndicator)

    impact_theme = mongoengine.EmbeddedDocumentField(ImpactThemes)
    # Also sometimes called "Sustainable goods and services. Each one should relate to a single imact theme."
    sustainable_products_and_services = mongoengine.ListField(mongoengine.StringField)

    #Carbon Footprint & Energy Transition Data: Global Score Energy Transition
    # On a scale from 0 to 100
    energy_transition_score = mongoengine.IntField()
