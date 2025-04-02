package com.hades.discord.bot.carol.database

import io.ktor.client.*
import io.ktor.client.engine.okhttp.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.*
import kotlinx.serialization.json.*

class CarolDatabaseHelper(
    private val supabaseUrl: String,
    private val supabaseKey: String
) {
    @OptIn(ExperimentalSerializationApi::class)
    @PublishedApi
    internal val client = HttpClient(OkHttp) {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
                explicitNulls = false
                coerceInputValues = true
            })
        }
    }

    suspend fun <T> save(
        table: String,
        obj: T,
        serializer: SerializationStrategy<T>
    ) {
        val response = client.post("$supabaseUrl/rest/v1/$table") {
            header("apikey", supabaseKey)
            header("Authorization", "Bearer $supabaseKey")
            contentType(ContentType.Application.Json)
            header("Prefer", "resolution=merge-duplicates")
            setBody(Json.encodeToString(serializer, obj))
        }

        when (response.status) {
            HttpStatusCode.Created -> println("Registro criado")
            HttpStatusCode.OK -> println("Registro atualizado")
            else -> println("Status inesperado: ${response.status}")
        }
    }

    suspend fun <T> get(
        table: String,
        id: Long,
        deserializer: DeserializationStrategy<T>
    ): T? {
        return try {
            val response = client.get("$supabaseUrl/rest/v1/$table?id=eq.$id") {
                header("apikey", supabaseKey)
                header("Authorization", "Bearer $supabaseKey")
                accept(ContentType.Application.Json)
            }

            val jsonText = response.bodyAsText()
            println(jsonText)

            if (jsonText.length <= 3) {
                return null
            }

            when {
                jsonText.startsWith('[') -> {
                    Json.decodeFromString(deserializer, jsonText.substring(1, jsonText.length - 1))
                }
                jsonText.startsWith('{') -> {
                    Json.decodeFromString(deserializer, jsonText)
                }
                else -> null
            }
        } catch (e: Exception) {
            println("Erro ao buscar: ${e.message}")
            null
        }
    }

    suspend fun <T> updateColumn(
        table: String,
        id: Long,
        column: String,
        newValue: T,
        serializer: SerializationStrategy<T>
    ) {
        val jsonObject = buildJsonObject {
            put(column, Json.encodeToJsonElement(serializer, newValue))
        }

        client.patch("$supabaseUrl/rest/v1/$table?id=eq.$id") {
            header("apikey", supabaseKey)
            header("Authorization", "Bearer $supabaseKey")
            contentType(ContentType.Application.Json)
            setBody(jsonObject.toString())
        }.also { response ->
            if (!response.status.isSuccess()) {
                println("Erro ao atualizar: ${response.status}")
            }
        }
    }

    inline suspend fun <reified T : @Serializable Any> save(table: String, obj: T) {
        save(table, obj, serializer())
    }

    inline suspend fun <reified T : @Serializable Any> get(table: String, id: Long): T? {
        return get(table, id, serializer())
    }

    inline suspend fun <reified T : @Serializable Any> updateColumn(
        table: String,
        id: Long,
        column: String,
        newValue: T
    ) {
        updateColumn(table, id, column, newValue, serializer())
    }
}