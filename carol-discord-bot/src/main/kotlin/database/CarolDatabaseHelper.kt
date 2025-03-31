package com.hades.discord.bot.carol.database

import com.fasterxml.jackson.core.JsonParser
import com.fasterxml.jackson.core.JsonProcessingException
import com.fasterxml.jackson.core.StreamReadFeature
import com.fasterxml.jackson.databind.DeserializationFeature
import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.databind.SerializationFeature
import com.fasterxml.jackson.module.kotlin.jacksonObjectMapper
import com.fasterxml.jackson.module.kotlin.readValue
import com.hades.discord.bot.carol.CarolProperties
import io.ktor.client.*
import io.ktor.client.engine.okhttp.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json
import com.fasterxml.jackson.module.kotlin.registerKotlinModule

class CarolDatabaseHelper {
    companion object {
        val client = HttpClient(OkHttp) {
            install(ContentNegotiation) {
                json(Json {
                    ignoreUnknownKeys = true
                    isLenient = true
                    prettyPrint = true
                })
            }
        }

        suspend inline fun <reified T : Any> insertOrModifyExisting(table: String, id: Long, newMemb: T) {
            val exist: Boolean = if (get<T>(table, id) == true) true else false
            if (exist) {
                insert(table, newMemb)
            } else {
                update(table, id, newMemb)
            }
        }

        suspend inline fun <reified T : Any> get(table: String, id: Long): T? {
            try {
                // 1. Use GET em vez de POST para consultas
                val response = client.get("${CarolProperties.getSupabaseUrl()}/rest/v1/$table?id=eq.$id") {
                    headers {
                        append("apikey", CarolProperties.getSupabaseKey())
                        append("Authorization", "Bearer ${CarolProperties.getSupabaseKey()}")
                        append("Accept", "application/json")
                    }
                }

                // 2. Verifique o status da resposta
                if (!response.status.isSuccess()) {
                    println("Erro na resposta: ${response.status}")
                    return null
                }

                // 3. Trate a resposta como array (Supabase sempre retorna arrays)
                val responseBody = response.bodyAsText()
                val mapper = jacksonObjectMapper()
                    .configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false)

                val items: List<T> = mapper.readValue(
                    responseBody,
                    mapper.typeFactory.constructCollectionType(List::class.java, T::class.java)
                )

                // 4. Retorne o primeiro item ou null se vazio
                return items.firstOrNull()
            } catch (e: Exception) {
                println("Erro ao buscar membro: ${e.message}")
                e.printStackTrace()
                return null
            }
        }

        suspend fun <T : Any> insert(table: String, member: T) {
            val mapper = ObjectMapper().apply {
                registerKotlinModule()
                disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
            }

            try {
                // 1. Serialização segura
                val jsonBody = mapper.writeValueAsString(member)
                println("JSON a ser enviado: $jsonBody")

                // 2. Configuração da requisição
                val response = client.post("${CarolProperties.getSupabaseUrl()}/rest/v1/$table") {
                    headers {
                        append("apikey", CarolProperties.getSupabaseKey())
                        append("Authorization", "Bearer ${CarolProperties.getSupabaseKey()}")
                        append("Content-Type", "application/json")
                        append("Prefer", "return=representation")
                    }
                    setBody(jsonBody)
                }

                // 3. Análise da resposta
                when (response.status.value) {
                    in 200..299 -> {
                        println("Inserção bem-sucedida!")
                        println("Resposta: ${response.bodyAsText()}")
                    }
                    400 -> {
                        println("Erro 400 - Bad Request:")
                        println("Corpo enviado: $jsonBody")
                        println("Resposta do servidor: ${response.bodyAsText()}")
                    }
                    else -> {
                        println("Erro na inserção: ${response.status}")
                        println("Detalhes: ${response.bodyAsText()}")
                    }
                }
            } catch (e: JsonProcessingException) {
                println("Erro na serialização do objeto:")
                println("Tipo do objeto: ${member::class.java}")
                e.printStackTrace()
            } catch (e: Exception) {
                println("Erro geral na inserção:")
                e.printStackTrace()
            }
        }

        suspend fun <T : Any> update(table: String, id: Long, newMember: T) {
            try {
                val mapper = jacksonObjectMapper().apply {
                    registerKotlinModule()
                    disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
                }

                // Serializa o objeto para JSON
                val jsonBody = mapper.writeValueAsString(newMember)
                println("JSON sendo enviado: $jsonBody")

                val response = client.patch("${CarolProperties.getSupabaseUrl()}/rest/v1/$table?id=eq.$id") {
                    headers {
                        append("apikey", CarolProperties.getSupabaseKey())
                        append("Authorization", "Bearer ${CarolProperties.getSupabaseKey()}")
                        append("Content-Type", "application/json")
                        append("Prefer", "return=representation")
                    }
                    setBody(jsonBody)  // Use setBody em vez de parameter
                }

                when {
                    response.status.isSuccess() -> {
                        println("✅ Atualização bem-sucedida!")
                        println("Resposta: ${response.bodyAsText()}")
                    }
                    response.status.value == 400 -> {
                        println("❌ Erro 400 - Bad Request")
                        println("Possíveis causas:")
                        println("- Estrutura do JSON inválida")
                        println("- Tipos de dados incompatíveis")
                        println("- Valores ausentes para colunas NOT NULL")
                        println("Corpo enviado: $jsonBody")
                        println("Resposta do servidor: ${response.bodyAsText()}")
                    }
                    else -> {
                        println("Erro na atualização: ${response.status}")
                        println("Detalhes: ${response.bodyAsText()}")
                    }
                }
            } catch (e: JsonProcessingException) {
                println("Erro na serialização do objeto:")
                println("Tipo do objeto: ${newMember::class.java}")
                e.printStackTrace()
            } catch (e: Exception) {
                println("Erro geral na atualização:")
                e.printStackTrace()
            }
        }
    }
}