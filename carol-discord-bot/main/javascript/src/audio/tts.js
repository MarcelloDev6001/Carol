const fs = require("fs");
const gTTS = require("gtts");

class TTS {
  static createTTSFile(text = "", language = "pt-BR", outputFolder = "") {
    var gtts = new gTTS(text, language);
    gtts.save(outputFolder, function (err, result) {
      if (err) {
        throw new Error(err);
      }
      console.log(`Success! Open file ${outputFolder} to hear result.`);
      return;
    });
  }
}

module.exports = TTS;
