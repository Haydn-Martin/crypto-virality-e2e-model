from pathlib import Path

from sensai.featuregen import FeatureCollector
from sensai.sklearn.sklearn_regression import SkLearnRandomForestVectorRegressionModel, SkLearnLinearRegressionVectorRegressionModel
from sensai.xgboost import XGBGradientBoostedVectorRegressionModel

from .data import *
from .features import FeatureName, registry


def best_regression_model_storage_path(dataset: Dataset) -> Path:
    """
    Create a path for saving the best model.

    :param dataset: data used to train the model

    :return: dir used to store best model
    """
    return Path("results") / "models" / "regression" / dataset.tag() / "best_model.pickle"

class RegressionModelFactory:
    """
    A Factory class to produce instances of regression models.

    Methods:
        create_rf: Create an instance of a random forest regression model.
        create_linear: Create an instance of a linear regression model.
        create_xgb: Create an instance of a XGBoost regression model.
    """
    BASE_FEATURES = (FeatureName.NUMBER_PAGES, FeatureName.IMAGES_DENSITY, FeatureName.CHARACTERS_DENSITY,
        FeatureName.EQUATIONS_DENSITY)

    @classmethod
    def create_rf(cls, name_suffix="", min_samples_leaf=1, **kwargs):
        """
        Create an instance of a random forest regression model.

        :param name_suffix: model name
        :param min_samples_leaf: min samples required to be a leaf node

        :return: random forest model
        """
        fc = registry.collect_features(*cls.BASE_FEATURES)
        return SkLearnRandomForestVectorRegressionModel(min_samples_leaf=min_samples_leaf, **kwargs) \
            .with_feature_collector(fc) \
            .with_name(f"RandomForest{name_suffix}")

    @classmethod
    def create_linear(cls, name_suffix=""):
        """
        Create an instance of a linear regression model.

        :param name_suffix: model name

        :return: linear regression model
        """
        fc = registry.collect_features(*cls.BASE_FEATURES)
        return SkLearnLinearRegressionVectorRegressionModel() \
            .with_feature_collector(fc) \
            .with_feature_transformers(fc.create_feature_transformer_normalisation()) \
            .with_name(f"Linear{name_suffix}")

    @classmethod
    def create_xgb(cls, name_suffix="",
            min_child_weight: Optional[float] = None, **kwargs):
        """
        Create an instance of an XGBoost model.

        :param name_suffix: model name
        :param min_child_weight: minimum sum of instance weight (hessian) needed in a child

        :return: XGBoost regression model
        """
        fc = FeatureCollector(*cls.BASE_FEATURES)
        return XGBGradientBoostedVectorRegressionModel(min_child_weight=min_child_weight, **kwargs) \
            .with_feature_collector(fc) \
            .with_name(f"XGBoost{name_suffix}")