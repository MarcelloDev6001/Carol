import org.gradle.internal.impldep.com.amazonaws.PredefinedClientConfigurations.defaultConfig

plugins {
    kotlin("jvm") version "2.1.10"
    application
    kotlin("plugin.serialization") version "2.1.0"
}

group = "com.hades.discord.bot.carol"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}

dependencies {
    testImplementation(kotlin("test"))
    implementation("net.dv8tion:JDA:5.0.0-beta.10")
    implementation("club.minnced:jda-ktx:0.12.0")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin:2.15.0")
    implementation("com.fasterxml.jackson.core:jackson-databind:2.15.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")
    implementation(kotlin("stdlib"))

    // Dependências do Ktor (TODAS na mesma versão)
    implementation("com.squareup.okhttp3:okhttp:4.12.0")

    // Serialização JSON
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.0")

    // Corrotinas
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.3")

    implementation("io.ktor:ktor-client-core:2.3.7")
    implementation("io.ktor:ktor-client-okhttp:2.3.7") // Para Android/JVM
    implementation("io.ktor:ktor-client-content-negotiation:2.3.7")
    implementation("io.ktor:ktor-serialization-kotlinx-json:2.3.7")
}

tasks.test {
    useJUnitPlatform()
}

application {
    mainClass = "com.hades.discord.bot.carol.MainKt"  // Definindo a classe principal corretamente
}