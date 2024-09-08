const { Client, GatewayIntentBits } = require("discord.js");
const messageCreateEvent = require("./src/events/messageCreate.js");
const InteractionCreateEvent = require("./src/events/interactionCreate.js");

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers,
  ],
});

const { token } = require("./config.json");
const SlashComms = require("./deploy-commands.js");

client.once("ready", () => {
  console.log(`Bot ${client.user.tag} is online!`);
  SlashComms.initCommands();
});

// * when a message is sent
client.on("messageCreate", (message) => {
  const msg = new messageCreateEvent(message, client);
});

// * when you run a slash command
client.on("interactionCreate", async (interaction) => {
  if (!interaction.isCommand()) return;

  const interct = new InteractionCreateEvent(interaction);
});

// * finally, it starts the bot
client.login(token);
