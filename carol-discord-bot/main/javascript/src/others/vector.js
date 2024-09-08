class Vector2 {
  x = 0;
  y = 0;
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }
}

class Vector4 {
  x = 0;
  y = 0;
  z = 0;
  w = 0;
  constructor(x, y, z, w) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.w = w;
  }
}

module.exports = { Vector2, Vector4 };
