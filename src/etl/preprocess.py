import pandas as pd

class Preprocess:

    def __init__(self,df) -> None:
        self._df=df

    def preprocess_df(self):
        df_=self._df
        df_=df_[df_["age"] != "?"]
        df_=df_[df_["sex"] != "?"]
        df_=df_[df_["cp"] != "?"]
        #df_=df_[df_["trestbsp"] != "?"]
        df_=df_[df_["chol"] != "?"]
        df_=df_[df_["ca"] != "?"]
        df_=df_[df_["thal"] != "?"]

        return df_
