import pandas as pd

# kaggle
kaggle_csv_link = "https://gist.githubusercontent.com/EckoTan0804/7ba61515d185c6558f77504044b485bb/raw/4caac4c296138e0d40aa22c90ae38d712ba0531d/multiple_choice_responses_preprocessed.csv"
kaggle = pd.read_csv(kaggle_csv_link)

# glassdoor
url = 'https://drive.google.com/file/d/1--PxypVvP0YmyZLLKheD01sxigJTkn2h/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
glassdoor = pd.read_csv(path)
glassdoor = glassdoor.dropna(subset=["Country"])


def get_datasets():
    return kaggle, glassdoor
