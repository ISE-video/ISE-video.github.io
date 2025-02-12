import imageio
import glob
import numpy as np
from PIL import Image   # for resizing and cropping images


def process_image(img, mode):
    if mode == 'plan': # center-crop 128
        width, height = img.size
        new_width = new_height = 128
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2
        img = img.crop((left, top, right, bottom))
    elif mode == 'plan2': # center-crop 256
        width, height = img.size
        new_width = new_height = 256
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2
        img = img.crop((left, top, right, bottom))
    return img





def convert_to_gif():
    # recursively find all mp4 files in the current directory
    mp4_files = glob.glob('**/*.mp4', recursive=True)
    print(len(mp4_files))

    for mp4_file in mp4_files:
        print(mp4_file)

        # read the video file
        vid = imageio.get_reader(mp4_file,  'ffmpeg')
        # create a gif writer
        writer = imageio.get_writer(mp4_file[:-3]+ 'gif', fps=8, loop=48763)

        frames = []
        # iterate through the frames of the video
        for i, frame in enumerate(vid):
            # write the frame to the gif writer
            frames.append(frame)

        if "pick_bar" in mp4_file and "interaction" in mp4_file and "0" in mp4_file:
            frames = frames[:int(len(frames)/4)]

        vidlen = len(frames)
        stride = max(vidlen // 8, 1)

        # repeat last frame to make gif longer  
        for _ in range(4):
            img = Image.fromarray(frames[0])
            img = process_image(img, 'plan')
            writer.append_data(np.array(img))

        for i in range(0, vidlen, stride):
            # process the image
            img = Image.fromarray(frames[i])
            img = process_image(img, 'plan')
            writer.append_data(np.array(img))
            
        # repeat last frame to make gif longer  
        for _ in range(4 + (7- i // stride)):
            img = Image.fromarray(frames[-1])
            img = process_image(img, 'plan')
            writer.append_data(np.array(img))


        writer.close()
        print(mp4_file + ' converted to gif')



if __name__ == '__main__':
    convert_to_gif()