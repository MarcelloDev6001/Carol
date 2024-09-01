const Jimp = require("jimp");
const MainSettings = require("../mainsettings.js");

class ImageHelper {
  static async writeTextFittedToImage(input, text, output) {
    try {
      // Carrega a imagem
      const image = await Jimp.read(MainSettings.getFullPath(input));
      const imageWidth = image.bitmap.width;

      let font;
      let textWidth;

      // Loop para encontrar o tamanho da fonte que encaixa
      do {
        Jimp.loadFont(Jimp.FONT_SANS_64_BLACK);
        // textWidth = Jimp.me;

        // Reduz a fonte se o texto não couber na imagem
        if (textWidth > imageWidth) {
          text.font -= 8;
        }
      } while (textWidth > imageWidth && text.width > 8);

      // Adiciona o texto à imagem com a fonte ajustada
      image.print(font, 10, 10, text.text, imageWidth - 20);

      // Salva a imagem com o texto
      await image.writeAsync(MainSettings.getFullPath(output));

      console.log("Imagem processada e salva com o texto ajustado!");
      return true;
    } catch (error) {
      console.error("Erro ao processar a imagem:", error);
      return false;
    }
  }
}

class ImageText {
  constructor(text, color, size) {
    this.text = text;
    this.color = color;
    this.size = size;
  }
}

module.exports = { ImageHelper, ImageText };
