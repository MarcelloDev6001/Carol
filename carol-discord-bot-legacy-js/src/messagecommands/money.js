const MoneyConversion = require("../others/moneyconversion.js");

// * convert, for exemple: USD to BRL
class MoneyMessageCommand {
  static async money(message, prefix, messageCommand) {
    let args = message.content
      .replace(prefix, "")
      .replace(messageCommand + " ", "")
      .split(" ");
    if (args.length < 2) {
      message.reply(
        "Tem que ter moeda de origem, moeda de conversão e o valor."
      );
      return;
    }
    let amount = parseInt(args[2]);
    try {
      let finalResult = await MoneyConversion.fromTo(args[0], args[1], amount);
      message.reply(
        amount.toString() + " pra " + args[1] + " é " + finalResult
      );
    } catch (e) {
      message.reply("Ocorreu um erro: " + e);
    }
  }
}

module.exports = MoneyMessageCommand;
