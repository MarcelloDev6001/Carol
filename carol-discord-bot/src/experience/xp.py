import discord
import json
import os


class XPSystem:
    @staticmethod
    def get_file_path(user_id: int):
        return f"./data/usersdata/{str(user_id)}.json"

    @staticmethod
    async def get_xp(user: discord.Member, guild: discord.Guild):
        file_path = XPSystem.get_file_path(user.id)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                exp_json = json.load(file)
        else:
            exp_json = {}
        if guild.id not in exp_json:
            exp_json[guild.id] = {"xp": 0, "level": 0}
        return exp_json[guild.id]["xp"]

    @staticmethod
    async def get_level(user: discord.Member, guild: discord.Guild):
        file_path = XPSystem.get_file_path(user.id)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                exp_json = json.load(file)
        else:
            exp_json = {}
        if guild.id not in exp_json:
            exp_json[guild.id] = {"xp": 0, "level": 0}
        return exp_json[guild.id]["level"]

    @staticmethod
    async def update_experience_and_level(
        xp_to_add: int,
        level_to_add: int,
        message: discord.Message,
    ):
        file_path = XPSystem.get_file_path(message.author.id)
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                exp_json = json.load(file)
        else:
            exp_json = {}

        if message.guild.id not in exp_json:
            exp_json[message.guild.id] = {"xp": 0, "level": 0}

        exp_json[message.guild.id]["xp"] = exp_json[message.guild.id]["xp"] + xp_to_add

        if (
            exp_json[message.guild.id]["xp"]
            >= (exp_json[message.guild.id]["level"] + 1) * 1000
        ):
            exp_json[message.guild.id]["level"] = (
                exp_json[message.guild.id]["level"] + 1
            )
            level_up_embed = await XPSystem.get_level_up_embed(
                message.author,
                message.guild,
                exp_json[message.guild.id]["level"],
                exp_json[message.guild.id]["xp"],
            )
            await message.channel.send(
                content=f"<@{message.user.id}>", embed=level_up_embed
            )

        with open(file_path, "w") as file:
            json.dump(exp_json, file, indent=4)

        return exp_json

    @staticmethod
    async def get_users_rank(message: discord.Message, amount: int):
        users_in_folder = os.listdir("./data/usersdata/")
        users = []
        for user_file in users_in_folder:
            with open(f"./data/usersdata/{user_file}", "r") as file:
                element = json.load(file)
            if message.guild.id in element:
                users.append(
                    {
                        "memberID": user_file.replace(".json", ""),
                        "xp": element[message.guild.id]["xp"],
                        "level": element[message.guild.id]["level"],
                    }
                )

        users.sort(key=lambda x: x["xp"], reverse=True)
        return users[:amount]

    @staticmethod
    async def get_level_up_embed(user: discord.Member, user_level: int, user_xp: int):
        level_up_embed = discord.Embed(
            color=0xFFFFFF,
            title="Level UP!",
            description=f"Parabéns <@{user.id}>, você acabou de evoluir para o level {user_level}! ({user_xp} xp)",
        )
        level_up_embed.set_thumbnail(url=user.avatar.url)
        return level_up_embed
