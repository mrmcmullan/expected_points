import csv
import pygal
from scipy.interpolate import interp1d
import numpy as np

""" This project attempts to evaluate whether advancement on different 
portions of the football field is more valuable. It quanifies the values 
from a team's own goal line up to the opposing teams. It does this by 
looking at the average next score from data provided by nflscrapR in 
csv format. Further, this project attempts to uncover whether this method
of valuing yards correlates with the outcome of a game over the standard 
comparision of total yards"""

# Initiate list of list to store data for each down
yard_scores = [[0 for i in range(1,100)] for i in range(4)]
num_plays = [[0 for i in range(1,100)] for i in range(4)]
yard_values = [[0 for i in range(1,100)] for i in range(4)]

# Initiate lists to store counter for score type
off_td = [[0 for i in range(1,100)] for i in range(4)]
def_td = [[0 for i in range(1,100)] for i in range(4)]
off_fg = [[0 for i in range(1,100)] for i in range(4)]
def_fg = [[0 for i in range(1,100)] for i in range(4)]
off_safety = [[0 for i in range(1,100)] for i in range(4)]
def_safety = [[0 for i in range(1,100)] for i in range(4)]

# Loop to navigate thru available seasons
for year in range(2009, 2019):
	
	# Initiate filename that iterates thru every year
	filename = str(year) + '_reg_season_pbp.csv'
	
	# Load data
	with open(filename) as f:
		data = csv.reader(f)
		header_row = next(data)
		
		# Store data in list of lists to access w/ file closed
		pbp = []
		for row in data:			
			pbp.append(row)
	
	
	# Start loop through given year & intialize index counter
	index = -1
	for p in pbp:
		index += 1
		# Remove kickoffs, no plays, end of quarters, 
		# extra points, and two point conversions
		if (p[25] == 'kickoff' or p[25] == 'no_play'
			or p[25] == 'NA' or p[25] == 'qb_kneel'
			or p[25] == 'extra_point' or p[42] != 'NA'):
				continue
				
		# Specify down for given play
		if p[18] == '1':
			down = 1
		elif p[18] == '2':
			down = 2
		elif p[18] == '3':
			down = 3
		elif p[18] == '4':
			down = 4
		else:
			print('Error')
			print(index)
		
		# Establish what side of field team in possession has the ball
		yardline = p[21].split()
		# If on own side of field, yardline is number that follows side
		if p[4] == p[7]:
			yardline = 100 - int(yardline[1])
		elif p[6] == p[7]: 
			yardline = int(yardline[1])
		elif p[7] == 'MID':
			yardline = 50	
		

		# Attribute score on scoring play from the yard it originated
		# Identify whether home or away team had the ball
		if int(p[16]) == 1:
			if p[2] == p[4]:
				off_score_index = 50
				def_score_index = 51
			elif p[3] == p[4]:
				off_score_index = 51
				def_score_index = 50
			
			# Establish initial offensive and defensive scores
			orig_off_score = int(pbp[index-1][off_score_index])
			orig_def_score = int(pbp[index-1][def_score_index])
			
			# Identify new offensive and defensive scores on a scoring play,
			# calculate score change and attribute it to yardline
			new_off_score = int(p[off_score_index])
			new_def_score = int(p[def_score_index])
			score_diff = (new_off_score - orig_off_score) - (new_def_score - orig_def_score)
			
			# Identify score type on scoring plays and attribute to yardline
			if int(score_diff) == 6:
				off_td[down-1][yardline-1] += 1
			elif int(score_diff) == 3:
				off_fg[down-1][yardline-1] += 1
			elif int(score_diff) == -6:
				def_td[down-1][yardline-1] += 1
			elif int(score_diff) == -3:
				def_fg[down-1][yardline-1] += 1
			elif int(score_diff) == 2:
				off_safety[down-1][yardline-1] += 1
			elif int(score_diff) == -2:
				def_safety[down-1][yardline-1] += 1
			
			# Add points for extra points and two point conversion
			if int(score_diff) == 6:
				stop = 0
				for pat in pbp[index:]:
					stop += 1
					if pat[16] == '1' and pat[25] == 'extra_point':
						score_diff += 1
						break
					if play[16] == '1' and play[42] == 'success':
						score_diff += 2
						break
					if stop > 3:
						break
			yard_scores[down-1][yardline-1] += score_diff
			num_plays[down-1][yardline-1] += 1
			
			# No need to look for later scores
			continue 
			
			
		# Search for next score from a given non-scoring play
		# Identify whether home or away team had the ball
		if p[2] == p[4]:
			off_score_index = 50
			def_score_index = 51
		elif p[3] == p[4]:
			off_score_index = 51
			def_score_index = 50
		
		# Establish initial offensive and defensive scores
		orig_off_score = int(p[off_score_index])
		orig_def_score = int(p[def_score_index])
		game_id = int(p[1])
		
		# Search for next score
		for play in pbp[index:]:
			
			# Identify play where score changes
			if int(play[off_score_index]) != orig_off_score  or int(play[def_score_index]) != orig_def_score:
				
				# Attribute no score if half ends or game ends
				if play[24] == 'END QUARTER 2' or play[24] == 'END GAME':
					break
				
				# Calculate how much score changed
				else:
					new_off_score = int(play[off_score_index])
					new_def_score = int(play[def_score_index])
					score_diff = (new_off_score - orig_off_score) - (new_def_score - orig_def_score)
					
					# Identify score type on scoring plays and attribute to yardline
					if int(score_diff) == 6:
						off_td[down-1][yardline-1] += 1
					elif int(score_diff) == 3:
						off_fg[down-1][yardline-1] += 1
					elif int(score_diff) == -6:
						def_td[down-1][yardline-1] += 1
					elif int(score_diff) == -3:
						def_fg[down-1][yardline-1] += 1
					elif int(score_diff) == 2:
						off_safety[down-1][yardline-1] += 1
					elif int(score_diff) == -2:
						def_safety[down-1][yardline-1] += 1
					
					# Add points for extra points and two point conversion
					if int(score_diff) == 6:
						stop = 0
						for pat in pbp[index:]:
							stop += 1
							if pat[16] == '1' and pat[25] == 'extra_point':
								score_diff += 1
								break
							if play[16] == '1' and play[42] == 'success':
								score_diff += 2
								break
							if stop > 3:
								break
								
					yard_scores[down-1][yardline-1] += score_diff
					num_plays[down-1][yardline-1] += 1
					break

					
for down in range(4):	
	for yard in range(99):
		yard_values[down][yard] = yard_scores[down][yard] / num_plays[down][yard]
		off_td[down][yard] = off_td[down][yard] / num_plays[down][yard] * 100
		off_fg[down][yard] = off_fg[down][yard] / num_plays[down][yard] * 100
		def_td[down][yard] = def_td[down][yard] / num_plays[down][yard] * 100
		def_fg[down][yard] = def_fg[down][yard] / num_plays[down][yard] * 100
		off_safety[down][yard] = off_safety[down][yard] / num_plays[down][yard] * 100
		def_safety[down][yard] = def_safety[down][yard] / num_plays[down][yard] * 100
	


# Graph final		
x_label = [num for num in range(1,100)]
x_labels_maj = [num for num in range(5, 100, 5)]

# Write data to csv
with open("expected_points_data.csv", "w") as f:
	writer = csv.writer(f)
	writer.writerows(yard_values)


exp_value = pygal.Line(show_minor_x_labels=False, truncate_label=-1, x_title = 'Yards from Opponents Endzone', y_title = 'Expected Points', label_font_size=3)
exp_value.title = 'Expected Points From Each Yardline in the NFL'
exp_value.x_labels = x_label
exp_value.x_labels_major = x_labels_maj
exp_value.add( 'First Down', yard_values[0])
exp_value.add( 'Second Down', yard_values[1])
exp_value.add( 'Third Down', yard_values[2])
exp_value.add( 'Fourth Down', yard_values[3])
exp_value.render_to_file('value_of_yards_nfl.svg')

score_type_first = pygal.Line(legend_at_bottom=True, show_minor_x_labels=False, truncate_label=-1, x_title = 'Yards from Opponents Endzone', y_title = 'Probability in %', label_font_size=3)
score_type_first.title = 'Probabilities of Type of Next Score From First Down'
score_type_first.x_labels = x_label
score_type_first.x_labels_major = x_labels_maj
score_type_first.add('Offense Scores TD', off_td[0])
score_type_first.add('Defense Scores TD', def_td[0])
score_type_first.add('Offense Scores FG', off_fg[0])
score_type_first.add('Defense Scores FG', def_fg[0])
score_type_first.add('Safety Against Defense', off_safety[0])
score_type_first.add('Safety Against Offense', def_safety[0])
score_type_first.render_to_file('next_score_type_first_nfl.svg')

score_type_second = pygal.Line(legend_at_bottom=True, show_minor_x_labels=False, truncate_label=-1, x_title = 'Yards from Opponents Endzone', y_title = 'Probability in %', label_font_size=3)
score_type_second.title = 'Probabilities of Type of Next Score From Second Down'
score_type_second.x_labels = x_label
score_type_second.x_labels_major = x_labels_maj
score_type_second.add('Offense Scores TD', off_td[1])
score_type_second.add('Defense Scores TD', def_td[1])
score_type_second.add('Offense Scores FG', off_fg[1])
score_type_second.add('Defense Scores FG', def_fg[1])
score_type_second.add('Safety Against Defense', off_safety[1])
score_type_second.add('Safety Against Offense', def_safety[1])
score_type_second.render_to_file('next_score_type_second_nfl.svg')

score_type_third = pygal.Line(legend_at_bottom=True, show_minor_x_labels=False, truncate_label=-1, x_title = 'Yards from Opponents Endzone', y_title = 'Probability in %', label_font_size=3)
score_type_third.title = 'Probabilities of Type of Next Score From Third Down'
score_type_third.x_labels = x_label
score_type_third.x_labels_major = x_labels_maj
score_type_third.add('Offense Scores TD', off_td[2])
score_type_third.add('Defense Scores TD', def_td[2])
score_type_third.add('Offense Scores FG', off_fg[2])
score_type_third.add('Defense Scores FG', def_fg[2])
score_type_third.add('Safety Against Defense', off_safety[2])
score_type_third.add('Safety Against Offense', def_safety[2])
score_type_third.render_to_file('next_score_type_third_nfl.svg')

score_type_fourth = pygal.Line(legend_at_bottom=True, show_minor_x_labels=False, truncate_label=-1, x_title = 'Yards from Opponents Endzone', y_title = 'Probability in %', label_font_size=3)
score_type_fourth.title = 'Probabilities of Type of Next Score From Fourth Down'
score_type_fourth.x_labels = x_label
score_type_fourth.x_labels_major = x_labels_maj
score_type_fourth.add('Offense Scores TD', off_td[3])
score_type_fourth.add('Defense Scores TD', def_td[3])
score_type_fourth.add('Offense Scores FG', off_fg[3])
score_type_fourth.add('Defense Scores FG', def_fg[3])
score_type_fourth.add('Safety Against Defense', off_safety[3])
score_type_fourth.add('Safety Against Offense', def_safety[3])
score_type_fourth.render_to_file('next_score_type_fourth_nfl.svg')



# DOES EXPECTED POINTS FROM YARDS GAINED CORRELATE BETTER TO RESULTS THAN SIMPLY TOTAL YARDS
# WHERE IS WORSE SPOT TO TURN THE BALL OVER (ORIG EXP POINTS - NEW EXP POINTS)
