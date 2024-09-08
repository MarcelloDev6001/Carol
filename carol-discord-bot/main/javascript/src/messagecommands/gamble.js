const {
  EmbedBuilder,
  PermissionFlagsBits,
  DiscordAPIError,
  Message,
  MessagePayload,
  AttachmentBuilder,
} = require("discord.js");

class LetsGoGamblingCommand {
  // * the logic is simple
  // * it creates 3 random numbers and say "I CAN'T STOP WINNING" if they are equals, or else, it says "OH DANG IT"
  static async gamble(message, prefix, messageCommand) {
    message.reply("LET'S GO GAMBLING");
    let randomNumbersForGamble = [
      Math.floor(Math.random() * 10),
      Math.floor(Math.random() * 10),
      Math.floor(Math.random() * 10),
    ]; // * 3 random numbers
    let letsGoGamblingMessage = await message.channel.send(
      randomNumbersForGamble[0].toString()
    );
    function wait(ms, value) {
      return new Promise((resolve) => setTimeout(resolve, ms, value));
    }
    await wait(300, 0); // * wait 0.3 seconds
    await letsGoGamblingMessage.edit(
      new MessagePayload(message, {
        content:
          randomNumbersForGamble[0].toString() +
          " " +
          randomNumbersForGamble[1].toString(),
      })
    );
    await wait(300, 0); // * wait 0.3 seconds
    await letsGoGamblingMessage.edit(
      new MessagePayload(message, {
        content:
          randomNumbersForGamble[0].toString() +
          " " +
          randomNumbersForGamble[1].toString() +
          " " +
          randomNumbersForGamble[2].toString(),
      })
    );
    await wait(700, 0); // * wait 0.7 seconds
    if (
      randomNumbersForGamble[0] == randomNumbersForGamble[1] &&
      randomNumbersForGamble[0] == randomNumbersForGamble[2]
    ) {
      message.channel.send("I CAN'T STOP WINNING :smiley:");
    } else {
      message.channel.send("OH DANG IT :sob:");
    }
  }
}

module.exports = LetsGoGamblingCommand;
