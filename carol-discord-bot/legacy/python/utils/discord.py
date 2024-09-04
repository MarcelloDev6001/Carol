import discord
import typing

def auto_embed(*, title: str="", description: str="", url: str="", color=typing.Union[discord.Colour, int],fields={"": {}}, img_url: str="", thumbnail: str="", footer={"": ""}, artist={"": ""}):
    """
    Generate an embed, just this.

    Args:
        title: Embed title.
        description: Embed description.
        color: Embed color.
        fields: Embed fields (format are basically this: {"title": {"value": "something", "inline": False}})
        img_url: Embed Image URL
        thumbnail: Embed Thumbnail URL
        footer: Embed footer (format are basically this: {"text": "icon url"})
        artist: Embed Artist (format are basically this: {"name": {"url": "artist url", "icon": "artist icon"}})
    """

    embed = discord.Embed(title=title,description=description, colour=color, url=url)
    if fields != {"": {}}:
        for field in fields:
            embed.add_field(name=field, value=fields[field]["value"], inline=fields[field]["inline"])
    embed.set_image(url=img_url)
    embed.set_thumbnail(url=thumbnail)
    if footer != {"": ""} and len(footer) < 2:
        for foot in footer:
            embed.set_footer(text=foot, icon_url=footer[foot])
    if artist != {"": ""} and len(artist) < 2:
        for arts in artist:
            embed.set_author(name=arts, url=artist[arts]["url"], icon_url=artist[arts]["icon"])
    return embed
