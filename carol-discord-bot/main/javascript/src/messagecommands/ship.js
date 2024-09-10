const Jimp = require("jimp");
const JimpImage = require("../image/image");
const { Vector4, Vector2 } = require("../others/vector");
const { MessagePayload, AttachmentBuilder } = require("discord.js");
const fs = require("fs");

class ShipMessageCommand {
  static async ship(message, prefix, messageCommand) {
    let guildMembers = await message.guild.members.fetch();
    let members = guildMembers.map((u) => u.user.id);
    // console.log(members);
    let randomMemberToShipIndex = Math.floor(
      Math.random() * message.guild.memberCount
    );
    let randomMemberToShip = guildMembers.map((u) => u.user)[
      randomMemberToShipIndex
    ];
    // console.log(message.author);
    // console.log(randomMemberToShip);
    let shipPercent =
      (parseInt(message.author.id) + parseInt(randomMemberToShip.id)) % 100;
    let authorAvatarURL = "";
    let randomMemberToShipAvatarURL = "";
    if (randomMemberToShip["avatar"] == null) {
      randomMemberToShipAvatarURL =
        "https://th.bing.com/th/id/R.c09a43a372ba81e3018c3151d4ed4773?rik=KDIiur5iBWGt8w&pid=ImgRaw&r=0";
    } else {
      randomMemberToShipAvatarURL = `https://cdn.discordapp.com/avatars/${randomMemberToShip.id}/${randomMemberToShip.avatar}.png`;
    }
    if (
      message.author.avatar == null ||
      message.author.avatar == "" ||
      message.author.avatar == undefined
    ) {
      authorAvatarURL =
        "https://th.bing.com/th/id/R.c09a43a372ba81e3018c3151d4ed4773?rik=KDIiur5iBWGt8w&pid=ImgRaw&r=0";
    } else {
      authorAvatarURL = `https://cdn.discordapp.com/avatars/${message.author.id}/${message.author.avatar}.png`;
    }
    let userOneImage = new JimpImage(await Jimp.read(authorAvatarURL));
    let userTwoImage = new JimpImage(
      await Jimp.read(randomMemberToShipAvatarURL)
    );
    // console.log(authorAvatarURL);
    // console.log(randomMemberToShipAvatarURL);
    // console.log(shipPercent);

    let messageFinalContent = `<@${message.author.id}> + <@${randomMemberToShip.id}> = ${shipPercent} :heart:\n`;
    if (shipPercent >= 75) {
      messageFinalContent += "hmm, será que teremos um novo casal aq?";
      let baseShipImage = new JimpImage(
        await Jimp.read("./resources/images/messagecommands/ship/base_good.jpg")
      );
      userOneImage.resize(172, 172);
      userOneImage.rotate(-19);
      userOneImage.flip(true, false);
      userTwoImage.resize(172, 172);
      userTwoImage.rotate(2);
      baseShipImage.image.composite(userOneImage.image, 510, 174, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      baseShipImage.image.composite(userTwoImage.image, 345, 217, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      await baseShipImage.image.writeAsync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageFile = fs.readFileSync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageAttachment = new AttachmentBuilder(finalImageFile, {
        name: "ship.png",
      });
      message.channel.send(
        new MessagePayload(message, {
          content: messageFinalContent,
          files: [finalImageAttachment],
        })
      );
    } else if (shipPercent < 75 && shipPercent >= 50) {
      messageFinalContent += "é, talvez dê certo...";
      let baseShipImage = new JimpImage(
        await Jimp.read("./resources/images/messagecommands/ship/base_mid.jpg")
      );
      userOneImage.resize(60, 60);
      userTwoImage.resize(60, 60);
      userTwoImage.flip(true, false);
      baseShipImage.image.composite(userOneImage.image, 127, 55, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      baseShipImage.image.composite(userTwoImage.image, 301, 34, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      await baseShipImage.image.writeAsync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageFile = fs.readFileSync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageAttachment = new AttachmentBuilder(finalImageFile, {
        name: "ship.png",
      });
      message.channel.send(
        new MessagePayload(message, {
          content: messageFinalContent,
          files: [finalImageAttachment],
        })
      );
    } else if (shipPercent < 50 && shipPercent >= 30) {
      messageFinalContent += "acho que não vai dar certo esse casal...";
      let baseShipImage = new JimpImage(
        await Jimp.read(
          "./resources/images/messagecommands/ship/base_midlow.jpg"
        )
      );
      userOneImage.resize(60, 60);
      userTwoImage.resize(78, 78);
      userTwoImage.flip(true, false);
      baseShipImage.image.composite(userOneImage.image, 307, 73, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      baseShipImage.image.composite(userTwoImage.image, 109, 68, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      await baseShipImage.image.writeAsync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageFile = fs.readFileSync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageAttachment = new AttachmentBuilder(finalImageFile, {
        name: "ship.png",
      });
      message.channel.send(
        new MessagePayload(message, {
          content: messageFinalContent,
          files: [finalImageAttachment],
        })
      );
    } else if (shipPercent < 35) {
      messageFinalContent += "provavelmente não vão dar certo no futuro...";
      let baseShipImage = new JimpImage(
        await Jimp.read("./resources/images/messagecommands/ship/base_bad.jpg")
      );
      userOneImage.resize(108, 108);
      userOneImage.flip(true, false);
      userTwoImage.resize(108, 108);
      baseShipImage.image.composite(userOneImage.image, 381, 134, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      baseShipImage.image.composite(userTwoImage.image, 1402, 82, {
        mode: Jimp.BLEND_SOURCE_OVER,
        opacityDest: 1,
        opacitySource: 1,
      });
      await baseShipImage.image.writeAsync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageFile = fs.readFileSync(
        "./resources/images/messagecommands/ship/cache.jpg"
      );
      let finalImageAttachment = new AttachmentBuilder(finalImageFile, {
        name: "ship.png",
      });
      message.channel.send(
        new MessagePayload(message, {
          content: messageFinalContent,
          files: [finalImageAttachment],
        })
      );
    }
  }
}

module.exports = ShipMessageCommand;
