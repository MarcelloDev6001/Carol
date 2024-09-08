const { Client, GatewayIntentBits } = require("discord.js");
const messageCreateEvent = require("./src/events/messageCreate.js");
const InteractionCreateEvent = require("./src/events/interactionCreate.js");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
});

const { token } = require("./config.json");
const SlashComms = require("./deploy-commands.js");

client.once("ready", () => {
  console.log(`Bot ${client.user.tag} is online!`);
  SlashComms.initCommands();
});

client.on("messageCreate", (message) => {
  const msg = new messageCreateEvent(message, client);
});

client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  const interct = new InteractionCreateEvent(interaction);
});

client.login(token);
