const QRCode = require("qrcode");
const fs = require("fs");
const { MessagePayload, AttachmentBuilder } = require("discord.js");

// * self explanatory, right?
class QRCodeGenerator {
  static async qrcode(message, prefix, messageCommand) {
    let arg = message.content.replace(prefix + messageCommand + " ", "");
    if (arg == "" || arg == prefix + messageCommand + " ") {
      message.reply("tu tem que informar um texto");
      return;
    }
    let rickrollChance = Math.floor(Math.random() * 10);
    if (rickrollChance == 6) {
      // * it's simple, if the random number is 1, soo you will get rickrolled >:)
      await QRCodeGenerator.generateQRCode(
        "https://youtu.be/dQw4w9WgXcQ?si=rJb9-oWRTqgpBvmh",
        "./resources/images/qrcodes/cache.png"
      );
    } else {
      await QRCodeGenerator.generateQRCode(
        arg,
        "./resources/images/qrcodes/cache.png"
      );
    }
    function wait(ms, value) {
      return new Promise((resolve) => setTimeout(resolve, ms, value));
    }
    await wait(2000, 1); // * wait 2 seconds (the time aproximally required to save the QRCode image)
    let qrcodeFile = fs.readFileSync("./resources/images/qrcodes/cache.png");
    let qrcodeAttachment = new AttachmentBuilder(qrcodeFile, {
      name: "qrcode.png",
    });
    message.reply(
      new MessagePayload(message, {
        content: "aqui:",
        files: [qrcodeAttachment],
      })
    );
  }
  static async generateQRCode(text, fileOutput) {
    QRCode.toFile(fileOutput, text, function (err) {
      if (err) throw err;
      console.log("QR generated");
    });
  }
}

module.exports = QRCodeGenerator;
