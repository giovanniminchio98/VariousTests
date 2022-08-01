from pytube import YouTube
import os

if __name__ == '__main__':
    a=1
    # file we want to download
    yt = YouTube('https://www.youtube.com/watch?v=DXT9dF-WK-I&ab_channel=%E9%98%BF%E9%B2%8DAbao')
    # file ext choosen
    mp4_files = yt.streams.filter(file_extension="mp4")
    # video quality
    mp4_369p_files = mp4_files.get_by_resolution("360p")
    # where to save the video
    save_to = os.path.join(os.getcwd(), 'video youtube')
    # start the download (script will end once is finished)
    mp4_369p_files.download(save_to)
