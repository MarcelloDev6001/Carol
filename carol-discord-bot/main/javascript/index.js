const { Client, GatewayIntentBits } = require("discord.js");
const messageCreateEvent = require("./src/events/messageCreate.js");
const InteractionCreateEvent = require("./src/events/interactionCreate.js");
const readline = require("readline");

readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers,
  ],
});

const { token } = require("./config.json");
// const SlashComms = require("./deploy-commands.js");

client.once("ready", () => {
  console.log(`Bot ${client.user.tag} is online!`);
  // SlashComms.initCommands();
});

// * when a message is sent
client.on("messageCreate", (message) => {
  const msg = new messageCreateEvent(message, client);
});

// * when you run a slash command
client.on("interactionCreate", async (interaction) => {
  const interct = new InteractionCreateEvent(interaction);
});

process.stdin.on("keypress", async (str, key) => {
  if (key.name === "escape") {
    console.log(`turning off ${client.user.tag}`);
    await client.destroy();
    process.exit();
  }
});

// * finally, it starts the bot
client.login(token);
