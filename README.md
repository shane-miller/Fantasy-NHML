# Fantasy-NHML
### A machine learning based fantasy hockey draft helper.

#### Info:
- In order to handle player injuries or other misc reasons games had to be missed, the fantasy point value used for training will be the following equation:


  ![equation](https://latex.codecogs.com/gif.latex?a%20%3D%20%5Ctextrm%7Btotal%20number%20of%20fantast%20points%20earned%20in%20a%20season%7D)

  ![equation](https://latex.codecogs.com/gif.latex?b%20%3D%20%5Ctextrm%7Bnumber%20of%20games%20played%7D)

  ![equation](https://latex.codecogs.com/gif.latex?%280.4a%29%20&plus;%20%280.6%28%5Cfrac%7B82a%7D%7Bb%7D%29%29)

  or could be "simplified" to

  ![equation](https://latex.codecogs.com/gif.latex?%28%5Cfrac%7B2ab&plus;246a%7D%7B5b%7D%29)

#### How to Run:
- Run download_from_nhl_stats.py to download last 5 years of stats for active players to respective data folders.
