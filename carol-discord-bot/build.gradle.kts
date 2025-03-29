plugins {
    kotlin("jvm") version "2.1.10"
    application
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
    implementation(kotlin("stdlib"))
}

tasks.test {
    useJUnitPlatform()
}
kotlin {
    jvmToolchain(17)
}

application {
    mainClass = "com.hades.discord.bot.carol.MainKt"  // Definindo a classe principal corretamente
}