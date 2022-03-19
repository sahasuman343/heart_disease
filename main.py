
 #standard imports
import pandas as pd

from sklearn.model_selection import RepeatedKFold

# some helpful imports from sklearndf
from sklearndf.pipeline import ClassifierPipelineDF
from sklearndf.classification import RandomForestClassifierDF

# relevant FACET imports
from facet.data import Sample
from facet.selection import LearnerRanker, LearnerGrid

from src.etl.preprocess import Preprocess
from src.helper.run_manager import Run_manager
import src.helper.logger as logger

runmanager=Run_manager("test_run")
runmanager.create_output()
log=logger.logger(runmanager.dir_name)

log.info("Importing required Modules: Done")

# load the diabetes dataset
log.info("Loading the dataset")
diabetes_df = pd.read_csv('data/HEART.csv')

log.info("Preprocessing the dataset")
pp=Preprocess(diabetes_df)
diabetes_df=pp.preprocess_df()


# create FACET sample object
log.info("Creating the FACET object")
diabetes_sample = Sample(observations=diabetes_df, target_name="diagnosis")

log.info("Model Initialization")
# create a (trivial) pipeline for a random forest regressor
rnd_forest_reg = ClassifierPipelineDF(
    classifier=RandomForestClassifierDF(n_estimators=200, random_state=42)
)

# define grid of models which are "competing" against each other
rnd_forest_grid = [
    LearnerGrid(
        pipeline=rnd_forest_reg,
        learner_parameters={
            "min_samples_leaf": [8, 11, 15],
            "max_depth": [4, 5, 6],
        }
    ),
]

log.info("Model Selection")

# create repeated k-fold CV iterator
rkf_cv = RepeatedKFold(n_splits=5, n_repeats=10, random_state=42)

# rank your candidate models by performance (default is mean CV score - 2*SD)

log.info("Model Training")
ranker = LearnerRanker(
    grids=rnd_forest_grid, cv=rkf_cv, n_jobs=-3
).fit(sample=diabetes_sample)

log.info("Model Training: Done")


# get summary report
log.info(ranker.summary_report())

#ranker.best_model_.to_pickle("models/heart_rf.pkl")