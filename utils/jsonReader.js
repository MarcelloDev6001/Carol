const MainSettings = require("../mainsettings.js");
const fs = require('fs');

class JsonReader {
  static read(filePath) {
    fs.readFile(MainSettings.getFullPath(filePath), "utf8", (err, data) => {
      if (err) {
        console.error(`Erro ao ler o arquivo JSON: ${err}`);
        return;
      }

      try {
        // Analisa o conteúdo JSON
        const config = JSON.parse(data);
        if (mainSetts.printConfigs) {
          console.log("Configuração carregada:", config);
        }
        return config;
      } catch (parseError) {
        console.error(`Erro ao analisar o JSON: ${parseError}`);
        return null;
      }
    });
  }
}

module.exports = JsonReader;
