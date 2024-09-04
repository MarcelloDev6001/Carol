const fs = require("fs");

class JsonReader {
  static read(filePath) {
    // fs.readFile(filePath, { encoding: "utf8" }, (err, data) => {
    //   if (err) {
    //     console.error("Erro ao ler o arquivo:", err);
    //   }

    //   console.log(`File Path: ${filePath}`);
    //   console.log(`File Content: ${data}`);

    //   try {
    //     let obj = JSON.parse(data); // Analise o JSON
    //     return obj;
    //   } catch (e) {
    //     console.error("Erro ao analisar JSON:", e.message);
    //     return {};
    //   }
    // });
    try {
      let jsonData = fs.readFileSync(filePath, { encoding: "utf8" });
      // console.log(`File Path: ${filePath}`);
      // console.log(`File Content: ${jsonData}`);

      try {
        let obj = JSON.parse(jsonData); // Analise o JSON
        return obj;
      } catch (e) {
        console.error("Failed to parse JSON:", e.message);
        return {};
      }
    } catch (error) {
      console.log("Failed to read JSON file: " + error.message);
    }
  }

  static save(filePath, jsonObject) {
    try {
      fs.writeFileSync(filePath, JSON.stringify(jsonObject, null, 2));
    } catch (e) {
      console.log(`Error on save JSON: ${e.message}`);
    }
  }
}

module.exports = JsonReader;
