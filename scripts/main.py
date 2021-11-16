
import pandas as pd
import numpy as np

from eval_model import eval_model

df = pd.read_csv("../data/dataset_1.csv")

eval_model(df, 5)

