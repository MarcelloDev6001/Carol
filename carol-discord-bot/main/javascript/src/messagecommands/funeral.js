const {
  MessagePayload,
  GuildMember,
  User,
  Message,
  AttachmentBuilder,
} = require("discord.js");
const { Vector2 } = require("../others/vector");
const fs = require("fs");
const JimpImage = require("../image/image");
const Jimp = require("jimp");

class FuneralMessageCommand {
  static async funeral(message = Message, prefix, messageCommand) {
    let userThatDiedID = message.content
      .replace(prefix + messageCommand + " ", "")
      .trim()
      .split(" ")[0]
      .replace("<@", "")
      .replace(">", "");
    let userThatDied = await message.guild.members.fetch({
      user: [userThatDiedID],
      force: true,
    });
    console.log(userThatDied.get(userThatDiedID));
    let userThatDiedAvatarURL = `https://cdn.discordapp.com/avatars/${userThatDiedID}/${
      userThatDied.get(userThatDiedID)["user"].avatar
    }`;
    let userAvatarImage = new JimpImage(await Jimp.read(userThatDiedAvatarURL));
    userAvatarImage.resize(109, 109);
    userAvatarImage.rotate(13);
    let coffinImage = new JimpImage(
      await Jimp.read("./resources/images/messagecommands/funeral/base.jpg")
    );
    coffinImage = JimpImage.overlay(
      coffinImage.image,
      userAvatarImage.image,
      new Vector2(99, 17)
    );
    await coffinImage.writeAsync(
      "./resources/images/messagecommands/funeral/cache.jpg"
    );
    let finalImageFile = fs.readFileSync(
      "./resources/images/messagecommands/funeral/cache.jpg"
    );
    let finalImageAttachment = new AttachmentBuilder(finalImageFile, {
      name: "coffin.png",
    });
    message.reply(
      new MessagePayload(message, {
        content: `E hoje aqui estamos em nome do(a) <@${userThatDiedID.toString()}>, que morreu nessa manhã (<t:${Math.floor(
          Date.now() / 1000
        )}>)`,
        files: [finalImageAttachment],
      })
    );
  }
}

module.exports = FuneralMessageCommand;
