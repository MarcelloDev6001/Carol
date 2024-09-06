const QRCode = require("qrcode");

class QRCodeGenerator {
  static async generateQRCode(text, fileOutput) {
    QRCode.toFile(fileOutput, text, function (err) {
      if (err) throw err;
      console.log("QR generated");
    });
  }
}

module.exports = QRCodeGenerator;
