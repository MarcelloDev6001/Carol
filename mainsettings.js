const printConfigs = true;
const pathF = require("path");

class MainSettings {
  constructor() {
    this.printConfigs = printConfigs;
  }

  static getFullPath(path) {
    const configPath = pathF.join(__dirname, path);
    return configPath;
  }
}

module.exports = MainSettings;
