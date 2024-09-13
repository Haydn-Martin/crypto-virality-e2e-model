from enum import Enum

from sensai.data_transformation import DFTNormalisation, SkLearnTransformerFactoryFactory
from sensai.featuregen import FeatureGeneratorRegistry, FeatureGeneratorTakeColumns

from .data import *


class FeatureName(Enum):
    NUMBER_PAGES = "number_pages"
    IMAGES_DENSITY = "images_density"
    CHARACTERS_DENSITY = "characters_density"
    EQUATIONS_DENSITY = "equations_density"

registry = FeatureGeneratorRegistry()

registry.register_factory(FeatureName.NUMBER_PAGES, lambda: FeatureGeneratorTakeColumns(COL_NUMBER_PAGES,
    normalisation_rule_template=DFTNormalisation.RuleTemplate(
transformer_factory=SkLearnTransformerFactoryFactory.RobustScaler())))

registry.register_factory(FeatureName.IMAGES_DENSITY, lambda: FeatureGeneratorTakeColumns(COL_IMAGES_DENSITY,
    normalisation_rule_template=DFTNormalisation.RuleTemplate(
transformer_factory=SkLearnTransformerFactoryFactory.RobustScaler())))

registry.register_factory(FeatureName.CHARACTERS_DENSITY, lambda: FeatureGeneratorTakeColumns(COL_CHARACTERS_DENSITY,
    normalisation_rule_template=DFTNormalisation.RuleTemplate(
transformer_factory=SkLearnTransformerFactoryFactory.RobustScaler())))

registry.register_factory(FeatureName.EQUATIONS_DENSITY, lambda: FeatureGeneratorTakeColumns(COL_EQUATIONS_DENSITY,
    normalisation_rule_template=DFTNormalisation.RuleTemplate(
transformer_factory=SkLearnTransformerFactoryFactory.RobustScaler())))
