const { Client, GatewayIntentBits } = require("discord.js");
const Configs = require("./config.js");
const messageCreateEvent = require("./events/messageCreate.js");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const conf = new Configs();
const TOKEN = conf.token;

client.once("ready", () => {
  console.log(`Bot ${client.user.tag} está online!`);
});

client.on("messageCreate", (message) => {
  const msg = new messageCreateEvent(message, client);
});

client.login(TOKEN);
