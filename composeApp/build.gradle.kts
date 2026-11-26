import org.gradle.api.file.RelativePath
import org.jetbrains.compose.desktop.application.dsl.TargetFormat
import org.jetbrains.kotlin.gradle.ExperimentalWasmDsl
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.kotlinMultiplatform)
    alias(libs.plugins.androidLibrary)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
    alias(libs.plugins.kotlinSerialization)
}

// Single Source of Truth: Synchronisiere content/*.json und content/media/**/*.webp
// in generierte Build-Ressourcen (keine Kopien in Git).
val syncContentToComposeResources by tasks.registering(Sync::class) {
    from(rootProject.layout.projectDirectory.dir("content")) {
        include("*.json")
        into("files/content")
    }
    from(rootProject.layout.projectDirectory.dir("content/media")) {
        include("portraits/*.webp", "kapitel/*.webp", "schauplaetze/*.webp", "szenen/*.webp")
        eachFile {
            // Alle 167 Medien-IDs (Portraits, Kapitel, Schauplaetze, Einzelszenen) sind eindeutig
            // und werden flach als Compose DrawableResource unter drawable/<id>.webp bereitgestellt.
            relativePath = RelativePath(true, "drawable", name)
        }
        includeEmptyDirs = false
    }
    into(layout.buildDirectory.dir("generated/contentComposeResources"))
}

val syncContentToTestResources by tasks.registering(Sync::class) {
    from(rootProject.layout.projectDirectory.dir("content")) {
        include("*.json")
        into("content")
    }
    from(rootProject.layout.projectDirectory.dir("content/media")) {
        include("portraits/*.webp", "kapitel/*.webp", "schauplaetze/*.webp", "szenen/*.webp")
        into("media")
        includeEmptyDirs = false
    }
    into(layout.buildDirectory.dir("generated/testContentResources"))
}

kotlin {
    androidTarget {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_17)
        }
    }

    jvm("desktop") {
        compilerOptions {
            jvmTarget.set(JvmTarget.JVM_17)
        }
    }

    @OptIn(ExperimentalWasmDsl::class)
    wasmJs {
        outputModuleName.set("zwischenDenFronten")
        browser {
            commonWebpackConfig {
                outputFileName = "zwischenDenFronten.js"
            }
            testTask {
                enabled = false
            }
        }
        binaries.executable()
    }

    js(IR) {
        outputModuleName.set("zwischenDenFronten")
        browser {
            commonWebpackConfig {
                outputFileName = "zwischenDenFronten.js"
            }
            testTask {
                enabled = false
            }
        }
        binaries.executable()
    }

    sourceSets {
        val desktopMain by getting
        val desktopTest by getting

        commonMain.dependencies {
            implementation(compose.runtime)
            implementation(compose.foundation)
            implementation(compose.material3)
            implementation(compose.ui)
            implementation(compose.components.resources)
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
        }

        commonTest.dependencies {
            implementation(libs.kotlin.test)
        }

        androidMain.dependencies {
            implementation(libs.androidx.activity.compose)
        }

        desktopMain.dependencies {
            implementation(compose.desktop.currentOs)
            implementation(libs.kotlinx.coroutines.swing)
        }

        desktopTest.dependencies {
            implementation(libs.kotlin.test.junit)
        }

        val androidUnitTest by getting {
            dependencies {
                implementation(libs.kotlin.test.junit)
            }
        }

        desktopTest.resources.srcDir(
            syncContentToTestResources.map {
                layout.buildDirectory.dir("generated/testContentResources").get()
            }
        )
    }
}

compose.resources {
    publicResClass = true
    packageOfResClass = "de.pytales.zdf.resources"
    customDirectory(
        sourceSetName = "commonMain",
        directoryProvider = syncContentToComposeResources.map {
            layout.buildDirectory.dir("generated/contentComposeResources").get()
        }
    )
}

android {
    namespace = "de.pytales.zdf.shared"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        minSdk = libs.versions.android.minSdk.get().toInt()
    }

    sourceSets {
        getByName("test") {
            resources.srcDir(layout.buildDirectory.dir("generated/testContentResources"))
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

tasks.matching { it.name.contains("UnitTestJavaRes") }.configureEach {
    dependsOn(syncContentToTestResources)
}

compose.desktop {
    application {
        mainClass = "de.pytales.zdf.MainKt"

        nativeDistributions {
            targetFormats(TargetFormat.Msi, TargetFormat.Exe, TargetFormat.Deb)
            packageName = "Zwischen den Fronten"
            packageVersion = "1.0.0"
            description = "Historisches Zwei-Entscheidungs-Lernspiel (Alltag 1914–1919)"
            vendor = "PyTales Lernspiele"
        }
    }
}

tasks.withType<Test> {
    testLogging {
        events("passed", "skipped", "failed")
        showStandardStreams = true
    }
}
