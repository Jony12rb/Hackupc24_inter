import ffmpeg
import os


def make_video(image_names, audio_name, duration = 20, video_name = 'SampleData/output.mp4'):
    """
    Given a list of image names, an audio file, and a duration, creates a video with the images and audio.
    Each image will be displayed for the same amount of time (duration / number of images).
    """
    time_per_image = duration / len(image_names)
    with open('in.txt', 'w') as f:
        for image in image_names:
            f.write(f"file {image}\n")
            f.write(f"outpoint {time_per_image}\n")

    video = ffmpeg.input("in.txt", f = "concat")
    audio = ffmpeg.input(audio_name, t = duration)

    ffmpeg.output(video, audio, video_name).run()


    os.remove('in.txt')
    
    
if __name__ == '__main__':
    images = ["PngDataSet/IMG_4383.png", "PngDataSet/IMG_3723.png"]
    audio = "audio.mp3"
    t = 5
    make_video(images, audio, t)
    