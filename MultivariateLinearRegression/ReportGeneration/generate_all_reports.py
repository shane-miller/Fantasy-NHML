##### Predict and Save Fantasy Values #####
path = current_file_path.parents[0].parents[0] / 'Data' / 'PlayerData'

stats = np.load(path / 'most_recent_season_data.npy', allow_pickle=True)
stats = stats[0]

temp = []
for player in stats:
    temp.append([player[35], player[0], player[80], player[79], player[75], player[92], player[87], player[98],
                 player[136], player[131], player[140], player[31], player[170], player[169], player[152],
                 player[159], player[40], player[4]])
stats = temp

names = np.load(path / 'most_recent_season_data_names.npy', allow_pickle=True)
names = names[0]

predictions = []
temp = reg.predict(stats)
for i, player in enumerate(names):
    value = temp[i]
    if value < 0:
        value = 0
    else:
        value = math.ceil(value)

    predictions.append((player[0], value))

file = None
try:
    file = open(current_file_path.parents[0] / 'Reports' / 'center_report.txt', 'x')
except:
    os.remove(current_file_path.parents[0] / 'Reports' / 'center_report.txt')
    file = open(current_file_path.parents[0] / 'Reports' / 'center_report.txt', 'x')

max_name_len = max(len(player[0]) for player in predictions)
name_str = 'Player Name'
file.write(f'{name_str:>{max_name_len}}' + ' | ' + 'Predicted Fantasy Points' + '\n\n')

predictions.sort(key = lambda x: -x[1])
for player in predictions:
    file.write(f'{player[0]:>{max_name_len}}' + ' | ' + str(math.ceil(player[1])) + '\n')

file.close()