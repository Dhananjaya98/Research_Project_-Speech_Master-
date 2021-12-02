import moviepy.editor

video = moviepy.editor.VideoFileClip('speech.mp4')
audio = video.audio
audio.write_audiofile("sample.wav")
print("Completed the Separates !")
