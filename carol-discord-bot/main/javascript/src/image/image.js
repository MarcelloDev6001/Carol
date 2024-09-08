const Jimp = require("jimp");
const { Vector4, Vector2 } = require("../others/vector");

class JimpImage {
  image = null;
  constructor(image) {
    this.image = image;
  }

  resize(x = 1, y = 1) {
    this.image.resize(x, y);
  }

  crop(positions = Vector4) {
    this.image.crop(positions.x, positions.y, positions.z, positions.w);
  }

  rotate(angle = 0) {
    this.image.rotate(angle);
  }

  flip(flipX, flipY) {
    this.image.flip(flipX, flipY);
  }

  opacity(alpha = 0) {
    this.image.opacity(alpha);
  }

  greyscale() {
    this.image.greyscale();
  }

  blur(blurRadio = 0) {
    this.image.blur(blurRadio);
  }

  static overlay(
    image = JimpImage,
    overlayImage = JimpImage,
    position = Vector2
  ) {
    return image.composite(overlayImage, position.x, position.y, {
      mode: Jimp.BLEND_SOURCE_OVER,
      opacityDest: 1,
      opacitySource: 1,
    });
  }
}

module.exports = JimpImage;
