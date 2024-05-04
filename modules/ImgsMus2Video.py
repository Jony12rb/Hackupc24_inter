import ffmpeg
import os


def make_video(image_names : list[str], audio_name : str, duration : int = 20 , video_path : str = 'Data/ExampleData/test.mp4', size = 5712 ):
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

    ffmpeg.output(video, audio, video_path, s = "1024x1024",  vf = f"scale=w={size}:h={size}:force_original_aspect_ratio=1,pad={size}:{size}:(ow-iw)/2:(oh-ih)/2").run()

    os.remove('in.txt')
    
def make_video_experimental(image_names : list[str], audio_name : str, duration : int = 20 , video_path : str = 'Data/ExampleData/test.mp4', size = 5712 ):
    """
    Given a list of image names, an audio file, and a duration, creates a video with the images and audio.
    Each image will be displayed for the same amount of time (duration / number of images).
    """
    n = len(image_names)
    time_per_image = duration / n
    fade_duration = 0.1*time_per_image
    fade_out = time_per_image - fade_duration
    command = "ffmpeg"
    for image in image_names:
        command += f" -loop 1 -t {time_per_image} -i {image}  "
    command += f" -i {audio_name} -filter_complex \""
    for i in range(n):
        if i == 0:
            command += f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=out:st={fade_out}:d={fade_duration}[v{i}];"
        else:
            command += f"[{i}:v]scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,setsar=1,fade=t=in:st=0:d={fade_duration},fade=t=out:st={fade_out}:d={fade_duration}[v{i}];"
    for i in range(n):
        command += f"[v{i}]"
        
    command += f"concat=n={n}:v=1:a=0,format=yuv420p[v]\" -map \"[v]\" -map {n}:a -shortest {video_path}"
    
    os.system(command)
    
    
if __name__ == '__main__':
    images = ["Data/PngRealSet/IMG_4383.png", "Data/PngRealSet/IMG_3723.png", "Data/PngRealSet/IMG_3767.png"]
    audio = "Data/ExampleData/audio.mp3"
    t = 10
    print(make_video_experimental(images, audio, t))
    