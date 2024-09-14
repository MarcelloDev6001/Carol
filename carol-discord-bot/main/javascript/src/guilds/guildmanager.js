const JsonReader = require("../utils/jsonReader");

class GuildManager {
  static getConfig(guild) {
    let guildSettings = {};
    let guildSettingsTemplate = {
      prefix: "h.",
      timeout_enabled: true,
      timeout_max_messages: 5,
      timeout_max_time: 9,
      timeout_time: 60,
      audit_log_channel_id: 0,
      unauthorized_words: [],
    };
    try {
      guildSettings = JsonReader.read(
        `./data/guilds/settings/${guild.id}.json`
      );
    } catch (error) {
      guildSettings = guildSettingsTemplate;
    }
    if (guildSettings == {}) {
      guildSettings = guildSettingsTemplate;
    }
    for (const guildKey in guildSettingsTemplate) {
      if (!(guildKey in guildSettings)) {
        guildSettings[guildKey] = guildSettingsTemplate[guildKey];
      }
    }
    return guildSettings;
  }

  static saveConfig(guild, data = {}) {
    let guildSettingsTemplate = {
      prefix: "h.",
      timeout_enabled: true,
      timeout_max_messages: 5,
      timeout_max_time: 9,
      timeout_time: 60,
      audit_log_channel_id: 0,
      unauthorized_words: [],
    };
    for (const guildKey in guildSettingsTemplate) {
      if (!(guildKey in data)) {
        data[guildKey] = guildSettingsTemplate[guildKey];
      }
    }
    JsonReader.save(`./data/guilds/settings/${guild.id}.json`);
  }
}

module.exports = GuildManager;
