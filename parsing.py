import json

titles = {}
ratings = {}
episodes = {}


def get_show_names():
	with open('title.basics.tsv') as f:
		lines = f.readlines()
		for line in lines[1:]:
			line = line.rstrip('\n').split('\t')
			titles[line[0]] = line[2]


def get_ratings():
	# gets all the ratings data
	with open('title.ratings.tsv') as f:
		lines = f.readlines()
		for line in lines[1:]:
			line = line.rstrip('\n')
			show_id, rating, num_ratings = line.split('\t')
			ratings[show_id] = (float(rating), int(num_ratings))


def get_show_data():
	get_show_names()
	get_ratings()
	# gets all the show names data
	with open('title.episode.tsv', 'r') as f:
		lines = f.readlines()
		for line in lines[1:]:
			line = line.rstrip('\n')
			ep_id, show_id, season, ep_num = line.split('\t')

			# tries to cast episode number and season number to ints
			try:
				ep_num = int(ep_num)
			except ValueError:
				ep_num = None
			try:
				season = int(season)
			except ValueError:
				season = None

			try:
				rating, num_ratings = ratings[ep_id]
			except KeyError:
				rating = None
				num_ratings = None

			episodes.setdefault(show_id, {}).setdefault(season, {}).update({ep_id: {'ep_title': titles[ep_id],
																					'ep_num': ep_num,
																					'rating': rating,
																					'num_ratings': num_ratings}})

	with open('show_data.json', 'w') as f:
		f.write(json.dumps(episodes))

get_show_data()

names = {}
for show_id in titles:
	names[titles[show_id]] = show_id

with open('id_to_name_mapping.json', 'w') as f:
	f.write(json.dumps(titles))

with open('name_to_id_mapping.json', 'w') as f:
	f.write(json.dumps(names))
