const gTTS = require("gtts");

class TTS {
  // * simply create a audio file speaking the text with the google translator voice
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
