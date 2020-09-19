# Fantasy-NHML
### A machine learning based fantasy hockey draft helper.

#### Info:
- Predicts the upcoming year's fantasy values when given the player data from the previous years.
- In order to handle player injuries or other misc reasons games had to be missed, the scalable individual statistics and fantasy point value for skaters used for training will be extrapolated using the following equation:

  ![equation](https://latex.codecogs.com/gif.latex?a%20%3D%20%5Ctextrm%7Bstat%20value%7D)

  ![equation](https://latex.codecogs.com/gif.latex?b%20%3D%20%5Ctextrm%7Bnumber%20of%20games%20played%7D)

  ![equation](https://latex.codecogs.com/gif.latex?%280.4a%29%20&plus;%20%280.6%28%5Cfrac%7B82a%7D%7Bb%7D%29%29)

  or could be "simplified" to

  ![equation](https://latex.codecogs.com/gif.latex?%28%5Cfrac%7B2ab&plus;246a%7D%7B5b%7D%29)

#### How to Run:
- Run `pip3 install -r requirements.txt` to download the required modules. Feel free to remove the requirement for torch unless you want to mess with the VanillaDeepNetwork. It was added not really to be used, but rather to demonstrate that it would be much worse at predicting than the other algorithms.
- Run `python3 Data/DataDownloadScript/download_from_nhl_stats.py` from the base project folder. This will take some time as it is downloading the last 10 years of stats for players for training and the most recent seaon data to make the predictions from.
