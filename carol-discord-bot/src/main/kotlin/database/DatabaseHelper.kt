package com.hades.discord.bot.carol.database

import com.hades.discord.bot.carol.CarolProperties
import io.ktor.client.*
import io.ktor.client.engine.okhttp.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json

class DatabaseHelper {
    private val client = HttpClient(OkHttp) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
                isLenient = true
                prettyPrint = true
            })
        }
    }

    suspend fun insertMember(member: DiscordMember) {
        try {
            val response = client.post("${CarolProperties.getSupabaseUrl()}/rest/v1/discord_members") {
                headers {
                    append("apikey", CarolProperties.getSupabaseKey())
                    append("Authorization", "Bearer ${CarolProperties.getSupabaseKey()}")
                    append("Content-Type", "application/json")
                    append("Prefer", "return=representation")
                }
                setBody(member)
            }
            println("Resposta: ${response.bodyAsText()}")
        } catch (e: Exception) {
            println("Erro ao inserir membro: ${e.stackTraceToString()}")
        }
    }
}