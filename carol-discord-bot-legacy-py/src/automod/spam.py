import discord
from discord.ext import commands
import asyncio
import datetime


class SpamSystem:
    def __init__(self, limit=5, time=9000):
        self.spam_map = {}
        self.limit = limit
        self.time = time

    async def check_for_spam(self, user: discord.Member, message: discord.Message):
        user_id = user.id

        if user_id in self.spam_map:
            user_data = self.spam_map[user_id]
            last_message = user_data["last_message"]
            timer = user_data["timer"]
            difference = (
                message.created_at - last_message.created_at
            ).total_seconds() * 1000

            timer.cancel()  # Cancel the previous timer

            if difference < self.time:
                user_data["msg_count"] += 1
                if not user_data.get("messages"):
                    user_data["messages"] = []
                user_data["messages"].append(message)
                if user_data["msg_count"] >= self.limit:
                    try:
                        await user.timeout(
                            datetime.timedelta(0, 60)
                        )  # 60 seconds timeout
                        print(f"Member timeouted: {user.display_name}")
                    except discord.Forbidden:
                        # If the user cannot be timed out, handle the exception
                        print("Unable to timeout the user.")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    user_data["msg_count"] = 0
                    return True
                else:
                    user_data["timer"] = asyncio.get_event_loop().call_later(
                        self.time / 1000, self.spam_map.pop, user_id
                    )
                    self.spam_map[user_id] = user_data
            else:
                self.spam_map[user_id] = {
                    "msg_count": 1,
                    "last_message": message,
                    "timer": asyncio.get_event_loop().call_later(
                        self.time / 1000, self.spam_map.pop, user_id
                    ),
                }
        else:
            self.spam_map[user_id] = {
                "msg_count": 1,
                "last_message": message,
                "timer": asyncio.get_event_loop().call_later(
                    self.time / 1000, self.spam_map.pop, user_id
                ),
            }
        return False

    async def delete_spammed_messages(self, user):
        user_data = self.spam_map.get(user.id, {})
        user_spammed_messages = user_data.get("messages", [])
        for message in user_spammed_messages:
            try:
                await message.delete()
            except Exception as e:
                print(f"An error occurred while deleting a message: {e}")
