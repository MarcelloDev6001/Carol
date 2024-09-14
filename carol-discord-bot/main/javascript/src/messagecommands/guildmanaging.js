const GuildManager = require("../guilds/guildmanager");

class GuildManagingMessageCommands {
  static async setUnauthorizedWord(guild, word, message) {
    let guildSettings = GuildManager.getConfig(guild);
    guildSettings["unauthorized_words"].push([word]);
    GuildManager.saveConfig(guild, guildSettings);
    message.reply("Pronto");
  }

  static async setAuditLogChannel(guild, channel_id_str, message) {
    let guildSettings = GuildManager.getConfig(guild);
    let audit_log_channel_id = 0;
    let audit_log_channel = null;
    console.log(channel_id_str);
    try {
      audit_log_channel_id = Number(channel_id_str);
      audit_log_channel_id =
        audit_log_channel_id +
        Number(channel_id_str) / audit_log_channel_id -
        1;
      console.log(audit_log_channel_id);
      audit_log_channel = await guild.channels.fetch(audit_log_channel_id, {
        force: true,
      });
    } catch (error) {
      console.error("error:" + error.message);
      message.reply("Canal inválido");
      return;
    }
    guildSettings["audit_log_channel_id"] = audit_log_channel_id;
    GuildManager.saveConfig(guild, guildSettings);
    message.reply(`Novo canal de registros: <#${audit_log_channel_id}>`);
  }
}

module.exports = GuildManagingMessageCommands;
