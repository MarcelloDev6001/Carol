const fs = require("fs");

class JsonReader {
  // * read all the texts of a file and convert it to a dict {}
  static read(filePath) {
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
      return {};
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
