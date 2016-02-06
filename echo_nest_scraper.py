from pyechonest import *
import soundcloud


BLOG_SONGS_FILE = "blog_features.txt"
PER_BLOG_SONGS  = 10
BLOG_OUTPUT_FILE = "blog_vectors.txt"
SONG_OUTPUT_FILE = "song_vectors.txt"


config.ECHO_NEST_API_KEY="EOTNUCUCGL1YQCFLJ"
SOUNDCLOUD_CLIENT_ID = "8cdb95c116f052404a7aabf078e48a13"
DEFAULT_ASYNC_TIMEOUT = 30


def get_track_params(track_url, timeout = DEFAULT_ASYNC_TIMEOUT):
    # create client with access token
    client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_ID)
    track_obj = client.get('/resolve', url=track_url)
    sc_url = track_obj.uri
    
    # find api sc url
    url = sc_url+"/stream?client_id="+SOUNDCLOUD_CLIENT_ID
    
    t = track.track_from_url(url)
    song_entry = [t.id, t.danceability, t.energy, t.key, t.liveness, 
                  t.loudness, t.mode, t.speechiness, t.tempo]
    return song_entry

if __name__ == "__main__":
	f = open(BLOG_SONGS_FILE, "r")
	blog_file = open(BLOG_OUTPUT_FILE, "w")
	song_file = open(SONG_OUTPUT_FILE, "w")

	blog_params_map = {}

	lines = f.readlines()
	for l in lines:
		splits = l.split(" ")
		blog_id = splits[0]
		songs = splits[-1]
		agg_param_list = [0] * (len(splits) - 1)
		i = 0
		for song in songs.split("|"):
			s_param_list = get_track_params(song)
			s_param_list.insert(0, song)
			print ";".join([str(x) for x in s_param_list])
			song_file.write(";".join([str(x) for x in s_param_list]))
			song_file.flush()
			agg_param_list = [sum(x) for x in zip(agg_param_list, s_param_list[2:])]
			i = i + 1

		if i != 0:
			agg_param_list = [x*1.0/i for x in agg_param_list]
			agg_param_list_str = ";".join([str(x for x in agg_param_list)])
			blog_file.write(str(blog_id)+";"+agg_param_list_str)
			blog_file.flush()
			print str(blog_id)+";"+agg_param_list_str

	blog_file.flush()
	song_file.flush()


