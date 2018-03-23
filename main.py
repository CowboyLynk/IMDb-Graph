import matplotlib.pyplot as plt
import numpy as np
import json


print("Loading data... Please be patient.")

"""
with open('name_to_id_mapping.json', 'r') as f:
	name_to_id_mapping = json.loads(f.read())
"""
with open('id_to_name_mapping.json', 'r') as f:
	id_to_name_mapping = json.loads(f.read())

with open('show_data.json', 'r') as f:
	db = json.loads(f.read())
request = None


def get_ep_ratings(show_id):
	show = db[show_id]
	data_points = []
	for season in show:
		season = show[season]
		season_episodes = []
		for episode in season:
			episode = season[episode]
			season_episodes.append([episode['ep_num'], episode['rating'], episode["ep_title"]])

		data_points.append(season_episodes)
	return data_points


while request != 'quit':
	color_choices = ['magenta', 'red', 'blue', 'green', 'purple', 'cyan']
	show_id = input('Enter IMDb id: ')

	if show_id[0:2] == "tt":
		show_name = id_to_name_mapping[show_id]

	x = []
	y = []
	c = []

	try:
		ratings = get_ep_ratings(show_id)
	except KeyError:
		print('Show not found, please try again.')
		continue

	print("Showing data for:", show_name)
	print()

	episodes = []
	fig, ax = plt.subplots()

	ep_counter = 0
	for season_num, season in enumerate(ratings):

		try:
			color = color_choices[season_num % len(color_choices)]
			season.sort(key=lambda x: x[0])

			season_episodes = []
			for episode_num, episode in enumerate(season):
				if episode[1] is None:
					continue
				episode.append((season_num+1, episode_num+1))
				season_episodes.append(episode)
			episodes += season_episodes

			# linear regression stuff
			x_range = [x + ep_counter for x in range(len(season_episodes))]
			y_points = [x[1] for x in season_episodes if x[1]]
			if len(x_range) == 0:
				continue
			fit = np.polyfit(x_range, y_points, 1)
			fit_fn = np.poly1d(fit)
			plt.plot(x_range, [fit_fn(x) for x in x_range], color=color)

			x.extend(x_range)
			y.extend(y_points)
			c.extend([color for _ in range(len(season_episodes))])

			ep_counter += len(season)
		except:
			continue

	sc = plt.scatter(x, y, c=c)

	annot = ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points", color='white',
						bbox=dict(boxstyle="round", fc="w"),
						arrowprops=dict(arrowstyle="-"))
	annot.set_visible(False)


	def update_annot(ind):
		pos = sc.get_offsets()[ind["ind"][0]]
		annot.xy = pos
		text = "{}\nS{}E{}, Rating: {}".format(episodes[ind["ind"][0]][2], episodes[ind["ind"][0]][3][0],
											   episodes[ind["ind"][0]][3][1], episodes[ind["ind"][0]][1])
		annot.set_text(text)
		annot.get_bbox_patch().set_facecolor(c[ind["ind"][0]])
		annot.get_bbox_patch().set_alpha(0.9)


	def hover(event):
		vis = annot.get_visible()
		if event.inaxes == ax:
			cont, ind = sc.contains(event)
			if cont:
				update_annot(ind)
				annot.set_visible(True)
				fig.canvas.draw_idle()
			else:
				if vis:
					annot.set_visible(False)
					fig.canvas.draw_idle()


	fig.canvas.mpl_connect("motion_notify_event", hover)
	plt.title(show_name)
	plt.ylabel("IMDb Rating")
	plt.xlabel("Episode Number")

	plt.show()
