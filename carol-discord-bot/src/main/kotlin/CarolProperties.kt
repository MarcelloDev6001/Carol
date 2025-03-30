package com.hades.discord.bot.carol

import com.fasterxml.jackson.module.kotlin.*
import java.io.File

data class JsonConfig(
    val token: String,
    val applicationId: Long,
    val supabaseUrl: String,
    val supabaseKey: String,
    val databaseName: String,
    val databaseUsername: String,
    val databasePassword: String
)

class CarolProperties {
    companion object {
        private const val FILEPATH: String = "carol.properties.json"
        public fun readConfig(): JsonConfig {
            val mapper = jacksonObjectMapper()
            return mapper.readValue(File(FILEPATH), JsonConfig::class.java)
        }
        public fun getToken(): String {return readConfig().token }
        public fun getApplicationId(): Long {return readConfig().applicationId }
        public fun getSupabaseUrl(): String {return readConfig().supabaseUrl }
        public fun getSupabaseKey(): String {return readConfig().supabaseKey }
        public fun getDatabaseName(): String {return readConfig().databaseName }
        public fun getDatabaseUsername(): String {return readConfig().databaseUsername }
        public fun getDatabasePassword(): String {return readConfig().databasePassword }
    }
}