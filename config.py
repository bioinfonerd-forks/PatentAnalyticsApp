import os
from datetime import date


class Config(object):
    def __init__(self, debug=True):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, 'data')
        self.models_dir = os.path.join(self.base_dir, 'models')
        self.results_dir = os.path.join(self.base_dir, 'result')
        self.classifier_dir = os.path.join(self.base_dir, 'classifiers')
        self.model_name = '_feature_model.dill'
        self.matrix_name = '_feature_matrix.dill'
        self.art_units = (
            "36", "24", "21",
            # "16", "17", "26",
            # "28", "37"
        )

    def get_model_path(self, feature_name):
        return os.path.join(self.models_dir, feature_name + self.model_name)

    def get_matrix_path(self, feature_name):
        return os.path.join(self.data_dir, feature_name + self.matrix_name)

    def get_classifier_path(self, clf_name, rand=True):
        if rand:
            today = date.today().isoformat()
            return os.path.join(self.classifier_dir, clf_name + today + '.dill')
        else:
            return os.path.join(self.classifier_dir, clf_name + '.dill')
