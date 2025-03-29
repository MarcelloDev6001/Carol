package com.hades.discord.bot.carol.database

import com.hades.discord.bot.carol.CarolProperties
import com.hades.discord.bot.carol.JsonConfig
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody

object SupabaseManager {
    private val client = OkHttpClient()
    private val jsonMediaType = "application/json".toMediaType()
    private val properties: JsonConfig = CarolProperties.readConfig()

    fun get(table: String, id: String? = null): String {
        val url = if (id != null) {
            "${properties.supabaseUrl}/rest/v1/$table?id=eq.$id"
        } else {
            "${properties.supabaseUrl}/rest/v1/$table"
        }

        val request = Request.Builder()
            .url(url)
            .addHeader("apikey", properties.supabaseKey)
            .addHeader("Authorization", "Bearer ${properties.supabaseKey}")
            .addHeader("Accept", "application/json")
            .build()

        return client.newCall(request).execute().body?.string() ?: ""
    }

    suspend fun insert(table: String, jsonData: String): String {
        val body = jsonData.toRequestBody(jsonMediaType)

        val request = Request.Builder()
            .url("${properties.supabaseUrl}/rest/v1/$table")
            .addHeader("apikey", properties.supabaseKey)
            .addHeader("Authorization", "Bearer ${properties.supabaseKey}")
            .addHeader("Content-Type", "application/json")
            .addHeader("Prefer", "return=representation")
            .post(body)
            .build()

        return client.newCall(request).execute().body?.string() ?: ""
    }

    fun update(table: String, id: String, jsonData: String): String {
        val body = jsonData.toRequestBody(jsonMediaType)

        val request = Request.Builder()
            .url("${properties.supabaseUrl}/rest/v1/$table?id=eq.$id")
            .addHeader("apikey", properties.supabaseKey)
            .addHeader("Authorization", "Bearer ${properties.supabaseKey}")
            .addHeader("Content-Type", "application/json")
            .patch(body)
            .build()

        return client.newCall(request).execute().body?.string() ?: ""
    }

    fun delete(table: String, id: String): Boolean {
        val request = Request.Builder()
            .url("${properties.supabaseUrl}/rest/v1/$table?id=eq.$id")
            .addHeader("apikey", properties.supabaseKey)
            .addHeader("Authorization", "Bearer ${properties.supabaseKey}")
            .delete()
            .build()

        return client.newCall(request).execute().isSuccessful
    }
}