import ffmpeg
import os


def make_video(image_names : list[str], audio_name : str, duration : int = 20 , video_path : str = 'SampleData/output.mp4' ):
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

    ffmpeg.output(video, audio, video_path, vf = "scale=w=640:h=640:force_original_aspect_ratio=1,pad=640:640:(ow-iw)/2:(oh-ih)/2").run()

    os.remove('in.txt')
    
    
if __name__ == '__main__':
    images = ["PngDataSet/IMG_4383.png", "PngDataSet/IMG_3723.png", "PngDataSet/IMG_3767.png"]
    audio = "SampleData/audio.mp3"
    t = 5
    make_video(images, audio, t)
    