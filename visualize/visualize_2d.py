import cv2
import os

def images_to_video(folder_path, output_video_name=None, fps=30):
    """
    Converts a sequence of images in a folder to an MP4 video.

    Parameters:
        folder_path (str): Path to the folder containing images.
        output_video_name (str, optional): Name of the output video file. Defaults to the folder name.
        fps (int, optional): Frames per second for the output video. Defaults to 30.
    """
    # Use the folder name as the output video name if not provided
    if output_video_name is None:
        output_video_name = os.path.basename(os.path.normpath(folder_path)) + '.mp4'
    else:
        # Ensure the output file has .mp4 extension
        if not output_video_name.endswith('.mp4'):
            output_video_name += '.mp4'

    # Get a sorted list of image file names
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    image_files = sorted(image_files)

    if not image_files:
        print("No image files found in the specified folder.")
        return

    # Read the first image to get frame dimensions
    first_image_path = os.path.join(folder_path, image_files[0])
    frame = cv2.imread(first_image_path)
    if frame is None:
        print(f"Failed to read the image file {first_image_path}.")
        return

    height, width, channels = frame.shape
    frame_size = (width, height)

    # Define the codec and create VideoWriter object
    video_path = os.path.join(folder_path, output_video_name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 format
    video_writer = cv2.VideoWriter(video_path, fourcc, fps, frame_size)

    # Iterate over each image and write it to the video
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"Warning: Skipping unreadable image file {image_path}.")
            continue
        # Resize frame if it doesn't match the first image dimensions
        if (frame.shape[1], frame.shape[0]) != frame_size:
            frame = cv2.resize(frame, frame_size)
        video_writer.write(frame)

    # Release the VideoWriter object
    video_writer.release()
    print(f"Video saved successfully as {video_path}")