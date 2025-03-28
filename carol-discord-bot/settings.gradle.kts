plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "0.8.0"
}
rootProject.name = "carol-discord-bot"

dependencyResolutionManagement {
    versionCatalogs {
        create("libs") {
            library("deviousjda", "com.github.LorittaBot", "DeviousJDA").version("4153f3a5df")
        }
    }
}