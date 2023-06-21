from django.db import models
from django.core.exceptions import ValidationError
import re


class VideoMixin(models.Model):

    video_url = models.URLField(null=True, blank=True, help_text=
            "Supports links from YouTube or Vimeo like "
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ "
            "or https://vimeo.com/13020606")
    video_title = models.CharField(max_length=100)
    video_id = models.CharField(max_length=20, blank=True, null=True)
    video_service = models.CharField(max_length=20, blank=True, null=True)

    VIDEO_SERVICE_ID_REGEX = re.compile(
        r"(http:\/\/|https:\/\/|)(player.|www.)?"
        r"(vimeo\.com|youtu(be\.com|\.be|be\.googleapis\.com))"
        r"\/(video\/|embed\/|channels\/staffpicks\/|watch\?v=|v\/)?"
        r"([A-Za-z0-9._%-]*)?"
    )

    VIDEO_SERVICE_YOUTUBE = "youtube"
    VIDEO_SERVICE_VIMEO = "vimeo"

    error = (
        "Please enter a Youtube or Vimeo URL only, "
        "e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ or "
        "https://vimeo.com/13020606"
    )

    regex_error = (
        "The video URL appears to be invalid, please check that you copied "
        "it in its entirety."
    )

    @classmethod
    def parse_video_service(cls, video_url):
        """
        Determines which video service (YouTube or Vimeo) the URL is for.
        :param video_url:
        :return:
        """
        if "vimeo.com" in video_url:
            return cls.VIDEO_SERVICE_VIMEO
        elif (
            "youtube.com" in video_url
            or "youtu.be" in video_url
            or "youtube.googleapis.com" in video_url
        ):
            return cls.VIDEO_SERVICE_YOUTUBE

    @classmethod
    def parse_video_id(cls, video_url):
        """
        Retrieves the ID from a YouTube or Vimeo URL.

        To tweak or edit the regex you can do so at
        https://regex101.com/r/gdJ0pt/5

        Supported URL structures:
        http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
        http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
        https://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
        http://www.youtube.com/embed/0zM3nApSvMg?rel=0
        http://www.youtube.com/watch?v=0zM3nApSvMg
        http://youtu.be/0zM3nApSvMg
        https://youtube.googleapis.com/v/My2FRPA3Gf8
        https://vimeo.com/67736784
        https://vimeo.com/channels/staffpicks/242573626
        http://player.vimeo.com/video/25451551
        //player.vimeo.com/video/25451551

        :param video_url:
        :return:
        """
        m = cls.VIDEO_SERVICE_ID_REGEX.search(video_url)
        if m and m.group(6):
            return m.group(6)

    def __str__(self):
        return self.video_title
    
    def clean(self):
        video_url = self.video_url

        video_service = self.parse_video_service(video_url)
        if not video_service:
            raise ValidationError({"video_url": [self.error]})

        video_id = self.parse_video_id(video_url)
        if not video_id:
            raise ValidationError({"video_url": [self.regex_error]})

        self.video_id = video_id
        self.video_service = video_service
        super().clean()
    
    class Meta:
        abstract = True