import re;
import sys;
from youtube_transcript_api import YouTubeTranscriptApi;
import openai;
from sk import my_sk;


## get url for the video
urlPassed = sys.argv[1];
##urlPassed = '<a href="http://www.youtube.com/watch?v=NC2blnl0WTE">Some text</a>';
print(urlPassed);

def get_video_id(urlPassed):
	pattern = re.compile(r'(?:https?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtube|youtu|youtube-nocookie)\.(?:com|be)\/(?:watch\?v=|watch\?.+&v=|embed\/|v\/|.+\?v=)?([^&=\n%\?]{11})');
	## extract video id
	video_id = re.search(pattern, urlPassed).groups()[0];
	#print(video_id);
	return video_id;


def get_transcript(video_id):
	try:
		transcript = YouTubeTranscriptApi.get_transcript(video_id);
		#print(transcript);
		return transcript;
	except Exception as ex:
		print("could not get transcript from video id, exception: ", ex);
		return None;
	

def summarize(transcript):
	openai.api_key = my_sk;
	propmt = f"summarize the following transcript of a youtube video in an interesting way: \n\n{transcript}";

	response = openai.chat.completions.create(
		model="gpt-4o-mini",
		messages=[
			{"role":"system", "content":"You are a helpful assistant."},
			{"role":"user", "content":propmt}
		],
		temperature=0.25
	);

	#print(response);
	summary = response.choices[0].message.content;
	return summary;

def watch(urlPassed):
	video_id = get_video_id(urlPassed);
	transcript = get_transcript(video_id);
	##print(transcript);
	summary = summarize(transcript);
	print(summary);


watch(urlPassed);