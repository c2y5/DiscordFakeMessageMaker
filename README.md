# Usage - image.py

```py
from image import DiscordMessageImage

DMI = DiscordMessageImage(<user_id>, <text>) # EG: DMI = DiscordMessageImage(12345, "Hello World!")
img = DMI.create_image()
img.save(<name.ext>) # EG: img.save("test.png")
```

# Usage - main.py
- Edit line 27 of main.py to your own bot token
- Run main.py
