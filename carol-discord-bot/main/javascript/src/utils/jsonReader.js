const fs = require("fs");

class JsonReader {
  static async read(filePath) {
    fs.readFile(filePath, { encoding: "utf8" }, (err, data) => {
      if (err) {
        console.error("Erro ao ler o arquivo:", err);
      }

      console.log(`File Content: ${data}`);

      try {
        let obj = JSON.parse(data); // Analise o JSON
        return obj;
      } catch (e) {
        console.error("Erro ao analisar JSON:", e.message);
        return {};
      }
    });
  }

  static save(filePath, jsonContent) {
    try {
      fs.writeFile(
        filePath,
        JSON.stringify(jsonContent, null, 2),
        function (err) {
          if (err) throw err;
          console.log("Arquivo trocado!");
        }
      );
    } catch (e) {
      console.log(`error on save JSON: ${e}`);
    }
  }
}

module.exports = JsonReader;
