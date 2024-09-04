const {
  EmbedBuilder,
  PermissionFlagsBits,
  DiscordAPIError,
} = require("discord.js");
const JsonReader = require("../utils/jsonReader.js");
const { prefix } = require("../../config.json");

class SpamSystem {
  spamMap = new Map();
  LIMIT = 5;
  TIME = 9000;
  constructor(limit, time) {
    this.LIMIT = limit;
    this.TIME = time;
  }
  async checkForSpam(user, message) {
    if (this.spamMap.has(user.id)) {
      const userData = this.spamMap.get(user.id);
      const { lastMessage, timer } = userData;
      const difference =
        message.createdTimestamp - lastMessage.createdTimestamp;

      clearTimeout(timer);

      if (difference < this.TIME) {
        userData.msgCount += 1;
        if (userData.msgCount >= this.LIMIT) {
          try {
            await user
              .timeout(60000, "Spammou demais") // * 60000 = 60 seconds
              .then(console.log(`Member timeouted: ${user.displayName}`));
          } catch (error) {
            // ! maybe the "spammer" is a modder, so you can't timeout him
            console.error(error);
          }
          userData.msgCount = 0;
          return true;
        } else {
          userData.timer = setTimeout(() => {
            this.spamMap.delete(user.id);
          }, this.TIME);
          this.spamMap.set(user.id, userData);
        }
      } else {
        this.spamMap.set(user.id, {
          msgCount: 1,
          lastMessage: message,
          timer: setTimeout(() => {
            this.spamMap.delete(user.id);
          }, this.TIME),
        });
      }
    } else {
      const fn = setTimeout(() => {
        this.spamMap.delete(user.id);
      }, this.TIME);
      this.spamMap.set(user.id, {
        msgCount: 1,
        lastMessage: message,
        timer: fn,
      });
    }
    return false;
  }
}

module.exports = SpamSystem;
