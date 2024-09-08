const fs = require("fs");

class TXTReader {
  // * read all content of a file and returns it
  static read(filePath) {
    fs.readFile(filePath, { encoding: "utf8" }, (err, data) => {
      if (err) {
        console.error("Erro ao ler o arquivo:", err);
      }

      console.log(`File Content: ${data}`);
      return data;
    });
  }

  static save(filePath, content) {
    fs.writeFile(filePath, content, function (err) {
      if (err) throw err;
      console.log("Arquivo trocado!");
    });
  }
}

module.exports = TXTReader;
