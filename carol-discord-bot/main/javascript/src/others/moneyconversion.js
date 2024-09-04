const jQuery = require("jquery");

class MoneyConversion {
  static async fromTo(moneyType, moneyConversion, amount) {
    const url = `https://api.exchangerate-api.com/v4/latest/${moneyType.toUpperCase()}`;
    console.log(url);

    try {
      const response = await fetch(url);
      let data = await response.json();
      //   console.log(data);

      const tax = data["rates"][moneyConversion];

      return amount * tax;
    } catch (error) {
      console.error("Error on convert Money:", error);
    }
  }
}

module.exports = MoneyConversion;
