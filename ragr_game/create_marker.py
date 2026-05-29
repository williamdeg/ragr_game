from paths import BASE, ASSETS, PICS, FONTS
from PIL import Image, ImageDraw, ImageOps


def create_marker(pic_adr):

    frame = Image.open("pics\marker.png").convert("RGBA")
    player_pic = Image.open(pic_adr).convert("RGBA")

    frame_width = frame.width
    frame_height = frame.height
    padding = 2

    player_pic = ImageOps.fit(
        player_pic,
        (frame_width, frame_height),
        Image.Resampling.LANCZOS,
    )

    mask = Image.new("L", (frame_width, frame_height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse(
        (
            padding,
            padding,
            frame_width - padding,
            frame_height - padding,
        ),
        fill=255,
    )

    marker = Image.new("RGBA", (player_pic.width, player_pic.height), (0, 0, 0, 0))
    marker.paste(player_pic, mask=mask)
    marker.paste(frame, mask=frame)

    return marker
