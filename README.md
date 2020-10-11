# Fantasy-NHML
### A machine learning based fantasy hockey draft helper.

#### Info:
- Predicts the upcoming year's fantasy values when given the player data from the previous years.
- In the case of a shortened season, all players scalable stats will be scaled according to the maximum number of games played by any player in that shortened season.
  - Ex: If the max number of games played by any player in a shortened season was 41 games, then every player will have their stats multiplied by 2 (aka 82/41).
- In order to handle player injuries or other misc reasons games had to be missed, the scalable individual statistics and fantasy point value for skaters used for training will be extrapolated using the following equation:

  ![equation](https://latex.codecogs.com/gif.latex?a%20%3D%20%5Ctextrm%7Bstat%20value%7D)

  ![equation](https://latex.codecogs.com/gif.latex?b%20%3D%20%5Ctextrm%7Bnumber%20of%20games%20played%7D)

  ![equation](https://latex.codecogs.com/gif.latex?%280.4a%29%20&plus;%20%280.6%28%5Cfrac%7B82a%7D%7Bb%7D%29%29)

  or could be "simplified" to

  ![equation](https://latex.codecogs.com/gif.latex?%28%5Cfrac%7B2ab&plus;246a%7D%7B5b%7D%29)

#### How to Run:
- Run `pip3 install -r requirements.txt` to download the required modules.
- Run `python3 Data/DataDownloadScript/download_from_nhl_stats.py` from the base project folder. This will take some time as it is downloading the last 10 years of stats for players for training and the most recent seaon data to make the predictions from.
- Run `python3 run_all.py` from the base project folder. This generates the all the models to make predictions from.
  - If you want to run only specific models, you can add their tag in the command line. No tags will run them all, but if you add a tag it will only run the models tagged.
  - Tags are as follows:
    - `--mlr` for MultivariateLinearRegression
    - `--par` for PassiveAgressiveRegression
    - `--en` for ElasticNet
    - `--rf` for RandomForest
    - `--ab` for AdaBoost
    - `--gb` for GradientBoost
    - `--xgb` for XGBoost
