class SpamSystem {
  spamMap = new Map();
  LIMIT = 5;
  TIME = 9000;
  constructor(limit, time) {
    this.LIMIT = limit;
    this.TIME = time;
  }
  async checkForSpam(user, message) {
    // * the logic is simples:
    // * if you send more than {LIMIT} messages in {TIME}, you will get timeouted
    if (this.spamMap.has(user.id)) {
      const userData = this.spamMap.get(user.id);
      const { lastMessage, timer } = userData;
      const difference =
        message.createdTimestamp - lastMessage.createdTimestamp;

      clearTimeout(timer);

      if (difference < this.TIME) {
        userData.msgCount += 1;
        if (userData.messages == [] || userData.messages === undefined) {
          userData.messages = [];
        }
        userData.messages.push([message]);
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

  async deleteSpammedMessages(user) {
    let userSpammedMessages = this.spamMap.get(user.id).messages;
    for (let index = 0; index < userSpammedMessages.length; index++) {
      try {
        await userSpammedMessages[index].delete();
      } catch (e) {
        console.log(e);
      }
    }
  }
}

module.exports = SpamSystem;
