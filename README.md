# Fantasy-NHML
## A machine learning based fantasy hockey draft helper.

### Info:
- This project is designed to predict the upcoming year's fantasy values when given the player data from the previous years.
- In the case of a shortened season, all skaters scalable stats will be scaled according to the maximum number of games played by any player in that shortened season when extrapolated out to being a full 82 game season. Goalies are scaled as well, but only scales to a goalie max of 68 games (approximate max goalies play each year) assuming no goalie has reached 68 games.
  - Ex: If the max number of games played by any player in a shortened season was 41 games, then every player will have their stats multiplied by 2 (aka 82/41).
- In order to handle player injuries or other misc reasons games had to be missed, the scalable individual statistics and fantasy point value used for training will be extrapolated using the following equation:

  ![equation](https://latex.codecogs.com/gif.latex?a%20%3D%20%5Ctextrm%7Bstat%20value%7D)
  
  ![equation](https://latex.codecogs.com/gif.latex?b%20%3D%20%5Ctextrm%7Bnumber%20of%20games%20played%7D)
  
  ![equation](https://latex.codecogs.com/gif.latex?%280.5a%29%20&plus;%20%280.5%28%5Cfrac%7B82a%7D%7Bb%7D%29%29)
  
- This project implements a large amount of regression models and averages their guesses in an attempt to mitigate any mistakes or deficiencies that appear in any individual model. 
### How to Run:
- **Downloading Required Modules**
  - Run `pip3 install -r requirements.txt` to download the required modules.
- **Downloading Player Data History**
  - Run `python3 Data/DataDownloadScript/download_from_nhl_stats.py` from the base project folder. This will take some time as it is downloading the last 10 years of stats for players for training and the most recent seaon data to make the predictions from.
    - Add tags to set the point multipliers your league is using. You only need to set the tags if they are being used in your league as the opther tags will default to a multiplier of zero and will not be considered when making predictions. If you do not set any tags here, every prediction will be zero.
    - The tags for skaters are as follows:
      - `--g` for Goals
      - `--a` for Assists
      - `--pts` for Points
      - `--pm` for Plus/Minus
      - `--pim` for Penalty Minutes
      - `--ppg` for Power Play Goals
      - `--ppa` for Power play Assists
      - `--ppp` for Power Play Points
      - `--shg` for Short Handed Goals
      - `--sha` for Short Handed Assists
      - `--shp` for Short Handed Assists
      - `--gwg` for Game Winning Goals
      - `--fow` for Faceoffs Won
      - `--fol` for Faceoffs Lost
      - `--shft` for Shifts
      - `--sog` for Shots on Goal
      - `--hit` for Hits
      - `--blk` for Blocks
      - `--defp` for Defenceman Points
    - The tags for goalies are as follows:
      - `--gs` for Games Started
      - `--w` for Wins
      - `--l` for Losses
      - `--sa` for Shots Against
      - `--ga` for Goals Against
      - `--sv` for Saves
      - `--so` for Shutouts
      - `--otl` for Overtime Losses
    - Ex: For a league that gives players 3 fantasy points per goal, 2 per assist, and -1 per penalty minute and goalies 5 fantasy points per win, 3 extra for a shutout, and 2 for an overtime loss, you would run `python3 Data/DataDownloadScript/download_from_nhl_stats.py --g=3 --a=2 --pim=-1 --w=5 --so=3 --otl=2`.
- **Generate Models for Predictions**
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
    - Ex: To run only ElasticNet, AdaBoost, and XGBoost you would type `python3 run_all.py --en --ab --xgb`.
- **Generate Predictions**
  - Run `python3 generate_final_report.py` from the base project folder. This will generate a report of fantasy predictions in a new file named `final_report.txt`. That file will be in the base project folder.
    - If you do not want to use every model generated you can use the same tags as in the step above to limit what models are used for predictions. However, in order to use any given model it must have been previously generated with the `run_all.py` above. Providing no model tags will use all models for predictions.
    - There are three formats you can choose to have your final report generated with. The options are as follows:
      - `--format=sg` to Group Predictions Into Skater/Goalie Sections
      - `--format=fdg` to Group Predictions Into Forward/Defenceman/Goalie Sections (This is the Default if `--format` is Not Set)
      - `--format=cwdg` to Group Predictions Into Center/Wing/Defenceman/Goalie Sections
