import requests
import yt_dlp
import os
import ffmpeg
import asyncio
import datetime
import random
import re
import glob
import discord
import io

class VideoManager:
    def __init__(self, cache_size: int):
        self.cache_size = cache_size
        # tuple of (Level, time)
        self.normal_queue = asyncio.Queue(maxsize=cache_size)
        self.junkyard_queue = asyncio.Queue(maxsize=cache_size)
        self.cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

    async def start_cache(self):
        self._clear_cache()
        while True:
            normal_size = self.normal_queue.qsize()
            junkyard_size = self.junkyard_queue.qsize()
            if normal_size < self.cache_size or junkyard_size < self.cache_size: 
                video_infos = []
                # download enough videos to fully fill cache
                for _ in range(0, self.cache_size-normal_size):
                    video_infos.append(self._get_and_process_video(False))
                for _ in range(0, self.cache_size-junkyard_size):
                    video_infos.append(self._get_and_process_video(True))
                video_infos = await asyncio.gather(*video_infos)
                
                for video_info in video_infos:
                    if video_info[0] == None:
                        # if failed, delete any files it may have made
                        self._clear_time_from_cache(video_info[1])
                        continue
                    # if junkyard queue:
                    if video_info[2]:
                        await self.junkyard_queue.put((video_info[0], video_info[1]))
                        print(f"Added {video_info[0]["level_name"]} to the junkyard cache")
                    else:
                        await self.normal_queue.put((video_info[0], video_info[1]))
                        print(f"Added {video_info[0]["level_name"]} to the video cache")
                    
            await asyncio.sleep(1)
            
    # (Level, discord.File)
    async def get_level(self, include_junkyard, is_gif):
        info = None
        if include_junkyard:
            info = await self.junkyard_queue.get()
        else:
            info = await self.normal_queue.get()
        if is_gif:
            with open(os.path.join(self.cache_path, f"{info[1]}_loop.gif"), 'rb') as img:
                img_bytes = img.read()
            ret = (info[0], discord.File(io.BytesIO(img_bytes), filename=f"{info[1]}.gif"))
        else:
            with open(os.path.join(self.cache_path, f"{info[1]}_1.png"), 'rb') as img:
                img_bytes = img.read()
            ret = (info[0], discord.File(io.BytesIO(img_bytes), filename=f"{info[1]}.png"))

        self._clear_time_from_cache(info[1])
        return ret

    def _clear_cache(self):
        for file_name in os.listdir(self.cache_path):
            file_path = os.path.join(self.cache_path, file_name)
            os.remove(file_path)
    
    def _clear_time_from_cache(self, time):
        files = glob.glob(os.path.join(self.cache_path, f"{time}*"))
        for file in files:
            os.remove(file)

    async def _wait_for_file(self, file_name):
        file_path = os.path.join(self.cache_path, file_name)
        while not os.path.exists(file_path):
            await asyncio.sleep(0.1)

    async def _get_and_process_video(self, include_junkyard):
        # avoid levels having the same name in filesystem
        time = str(datetime.datetime.now(datetime.timezone.utc))
        time = re.sub('[^0-9]','', time)

        try:
            #video_info is (level_info, time, include_junkyard)
            video_info = await self._download_video(time, include_junkyard)
            video_time = video_info[1]

            video_path = self._get_path(video_time)
            duration, width, height = self._get_duration_and_width_and_heigh(video_path)
            frames = []
            for i in range(0, 3):
                random_video_time = random.uniform(0, duration)
                frames.append(self._get_frame(video_path, random_video_time, width, height, video_time+f"_{i+1}"))
            await asyncio.gather(*frames)
            await self._make_gif(video_time)
            return video_info
        except Exception as e:
            print(f"error: {e}")
            return (None, time, include_junkyard)

    async def _download_video(self, time, include_junkyard):
        try:
            url = f"http://localhost:8080/coretop/api/level/getRandomLevel?junkyard={include_junkyard}"
            response = requests.get(url)
            if response.status_code != 200:
                raise requests.exceptions.RequestException()
            level = response.json()

            print(f"TRYING {level["level_name"]} AT {time}")
            ydl_opts = {
                "quiet": True,
                "format": "bestvideo[height<=720]",
                "outtmpl": f"{self.cache_path}/{time}.%(ext)s",
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                await asyncio.to_thread(ydl.download, level["level_video"])
                return (level, time, include_junkyard)
        except Exception as e:
            print(f"Failed getting video: {e}")
        
    def _get_path(self, video_time):
        for ext in ['.mp4', '.webm']:
            path = os.path.join(self.cache_path, video_time + ext)
            if os.path.exists(path):
                return path
        return None

    def _get_duration_and_width_and_heigh(self, video_path):
        try:
            probe = ffmpeg.probe(video_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

            if not video_stream:
                raise Exception("video stream not found")
            if not "coded_width" in video_stream or not "coded_height" in video_stream:
                raise Exception("coded_width or coded_height not found")
            
            return (float(probe["format"]["duration"]), video_stream["coded_width"], video_stream["coded_height"])
        except ffmpeg.Error as e:
            print(f"Error probing video: {e.stderr.decode()}")
            raise e

    async def _get_frame(self, video_path, video_time, width, height, file_name):
        try:
            (
            ffmpeg
            .input(video_path, ss=video_time)
            .filter('crop', width // 2, (height // 10)*8, width // 2, height // 10)
            .output(os.path.join(self.cache_path, f"{file_name}.png"), vframes=1)
            .global_args("-loglevel", "error")
            .run_async()
            )
        except ffmpeg.Error as e:
            print(f"Error getting frame: {e.stderr.decode()}")
            raise e
    
    async def _make_gif(self, video_time):
        try:
            frames = []
            for i in range(1,4):
                await asyncio.wait_for(self._wait_for_file(f"{video_time}_{i}.png"), 2)
                frames.append(f"{self.cache_path}\\{video_time}_{i}.png")
            make_gif = await asyncio.subprocess.create_subprocess_exec(
                "C:\\Program Files\\gifski-1.32.0\\gifski.exe", "--fps", "1",
                "--quality", "100",
                "-o", f"{self.cache_path}\\{video_time}_loop.gif",
                *frames,
                stderr=asyncio.subprocess.PIPE
            )
            stderr = await make_gif.communicate()
            if make_gif.returncode != 0:
                raise Exception(stderr)
        except Exception as e:
            raise Exception(f"Failed to create gif: {e}")
        