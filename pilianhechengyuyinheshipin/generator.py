# -*- coding UTF-8 -*-
# @createDate 2023/8/2 11:08
# @Author 邓磊
# 指定要遍历的文件夹路径
import multiprocessing
import os
import threading

from moviepy.editor import VideoFileClip, AudioFileClip
import logging
# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# 创建文件处理器
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.ERROR)

# 添加格式化器
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# 将文件处理器添加到日志记录器
logger.addHandler(file_handler)

def make_video(audio_path, video_path, output_path):
    try:
        create_folder(output_path.replace(output_path.split("\\")[-1],""))
        # 读取视频文件
        video = VideoFileClip(video_path)

        # 读取音频文件
        audio = AudioFileClip(audio_path)

        # 将音频添加到视频中
        video_with_audio = video.set_audio(audio)

        # 将合并的视频保存为文件
        video_with_audio.write_videofile(output_path)
        # print(f"{output_path}合并完成")
    except Exception as e:
        print(f"{output_path}合并失败")
        print(e)
        logger.error(f"{output_path}合并失败")

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
def generator(path):
    folder_path = path
    file_path_list = []
    for filename in os.listdir(folder_path):
    # 拼接文件路径
        file_path = os.path.join(folder_path, filename)
        # 判断是否是文件夹
        if os.path.isdir(file_path):
            # 递归遍历文件夹中的文件
            generator(file_path)
        else:
            if file_path.endswith(".wav"):
                video_path = file_path.replace("\\audio", "\\video")
                video_path = video_path.replace(".wav", ".mp4")
                output_path = video_path.replace("\\video", "\\final")
                make_video(file_path, video_path, output_path)
            # # 打印文件路径
            # print(file_path)

if __name__ == '__main__':
    # generator(".\\audio\\s1")
    threads = []
    for i in range(1,7):
        path = f".\\audio\\s{i}"
        t = threading.Thread(target=generator, args=(path,))
        threads.append(t)

    # 启动所有线程
    for t in threads:
        t.start()

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("All threads have completed")