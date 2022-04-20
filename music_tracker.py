from yt_dlp import YoutubeDL
import discord
import asyncio

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0", 
}

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                    'options': '-vn'}

ytdl = YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

    @classmethod
    async def from_search(cls, search, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        asyncio.new_event_loop
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(f"ytsearch:{search}", download=not stream))
        if "entries" in data:
            data = data["entries"][0]
            
        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class MusicHandler:
    def __init__(self) -> None:
        self.play_queue = []

    def go_next(self):
        if len(self.play_queue) == 1:
            self.play_queue.pop(-1)
            return False
        elif len(self.play_queue) > 0:
            self.play_queue.pop(-1)
            self.play_obj(self.play_queue[-1][0], self.play_queue[-1][1])
            return True
        return False

    def play_obj(self, ctx, player):
        try:
            ctx.voice_client.play(player, after=lambda e: self.go_next())
        except:
            self.go_next()

    def queue_track(self, track_obj):
        if track_obj[1] == None or track_obj[0] == None:
            return False
        self.play_queue.insert(0, track_obj)