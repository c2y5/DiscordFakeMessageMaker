from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import json
from pilmoji import Pilmoji
from pilmoji.source import TwemojiEmojiSource
from datetime import datetime
import pytz
import textwrap

class DiscordMessageImage:
    def __init__(self, user_id, message, font_path="./ggsans.ttf"):
        self.user_id = user_id
        self.message = message
        self.font_path = font_path
        self.avatar_size = (40, 40)
        self.background_color = (28, 29, 34)
        self.username_color = (255, 255, 255)
        self.timestamp_color = (185, 187, 190)
        self.message_color = (220, 221, 222)
        
    def create_circular_mask(self, size):
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + size, fill=255)
        return mask

    def load_image_from_url(self, url):
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        return image

    def get_current_nzst_time(self):
        nzst = pytz.timezone('Pacific/Auckland')
        current_time = datetime.now(nzst)
        return current_time.strftime("%H:%M")

    def get_user_data(self):
        response = requests.get(url=f"https://discordlookup.mesalytic.moe/v1/user/{self.user_id}")
        return json.loads(response.text)

    def wrap_text(self, text, width):
        wrapped_text = textwrap.fill(text, width=width, break_long_words=True, replace_whitespace=False)
        return wrapped_text

    def create_image(self):
        user_data = self.get_user_data()
        avatar_url = f"{user_data['avatar']['link']}.png"
        username = user_data["global_name"]
        timestamp = f"Today at {self.get_current_nzst_time()}"

        avatar = self.load_image_from_url(avatar_url).resize(self.avatar_size, Image.LANCZOS)
        mask = self.create_circular_mask(self.avatar_size)
        avatar = avatar.convert("RGBA")
        avatar.putalpha(mask)

        wrapped_message = self.wrap_text(self.message, 58)
        line_count = len(wrapped_message.split("\n"))
        image_width = 410
        image_height = 70 + (18 * (line_count - 1))
        image = Image.new("RGB", (image_width, image_height), self.background_color)

        avatar_position = (10, 10)
        image.paste(avatar, avatar_position, mask=mask)

        username_font = ImageFont.truetype(self.font_path, 16)
        timestamp_font = ImageFont.truetype(self.font_path, 10)
        message_font = ImageFont.truetype(self.font_path, 14)

        draw = ImageDraw.Draw(image)

        username_position = (avatar_position[0] + self.avatar_size[0] + 10, avatar_position[1])
        username_bbox = draw.textbbox((0, 0), username, font=username_font)
        timestamp_bbox = draw.textbbox((0, 0), timestamp, font=timestamp_font)

        timestamp_y = username_position[1] + (username_bbox[3] - timestamp_bbox[3]) // 2 + 2.5
        timestamp_position = (username_position[0] + username_bbox[2] + 10, timestamp_y)

        message_position = (username_position[0], username_position[1] + username_bbox[3] + 5)

        with Pilmoji(image, source=TwemojiEmojiSource) as pilmoji:
            pilmoji.text(username_position, username, font=username_font, fill=self.username_color, emoji_position_offset=(0, 2))
            pilmoji.text(timestamp_position, timestamp, font=timestamp_font, fill=self.timestamp_color)
            pilmoji.text(message_position, wrapped_message, font=message_font, fill=self.message_color, emoji_scale_factor=1.4, emoji_position_offset=(0, 1))

        return image
