import org.gradle.api.GradleException
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.kotlinAndroid)
    alias(libs.plugins.composeMultiplatform)
    alias(libs.plugins.composeCompiler)
}

fun resolveReleaseOption(name: String): String? =
    providers.gradleProperty(name).orNull?.takeIf { it.isNotBlank() }
        ?: providers.environmentVariable(name).orNull?.takeIf { it.isNotBlank() }

// Konsistente Release-Versionierung (optional über Gradle-Property oder Env-Var überschreibbar)
val releaseVersionCode = resolveReleaseOption("ZDF_VERSION_CODE")?.toIntOrNull() ?: 10200
val releaseVersionName = resolveReleaseOption("ZDF_VERSION_NAME") ?: "1.2.0"

// Optionale Release-Signierung über Gradle-Properties oder Umgebungsvariablen
val releaseKeystorePath = resolveReleaseOption("ZDF_KEYSTORE_PATH")
val releaseKeystorePassword = resolveReleaseOption("ZDF_KEYSTORE_PASSWORD")
val releaseKeyAlias = resolveReleaseOption("ZDF_KEY_ALIAS")
val releaseKeyPassword = resolveReleaseOption("ZDF_KEY_PASSWORD")
val allowUnsignedRelease = resolveReleaseOption("ZDF_UNSIGNED_RELEASE")?.equals("true", ignoreCase = true) == true

val signingInputs = listOf(
    releaseKeystorePath,
    releaseKeystorePassword,
    releaseKeyAlias,
    releaseKeyPassword,
)
val anySigningSet = signingInputs.any { it != null }
val allSigningSet = signingInputs.all { it != null }

val releaseKeystoreFile = releaseKeystorePath?.let { rawPath ->
    val direct = file(rawPath)
    if (direct.isFile) direct else rootProject.file(rawPath)
}

if (anySigningSet && (!allSigningSet || releaseKeystoreFile == null || !releaseKeystoreFile.isFile)) {
    throw GradleException(
        "Unvollständige Android-Release-Signierung: Bitte alle vier Variablen setzen " +
            "(ZDF_KEYSTORE_PATH [existierende Keystore-Datei], ZDF_KEYSTORE_PASSWORD, " +
            "ZDF_KEY_ALIAS, ZDF_KEY_PASSWORD) oder alle leer lassen, um den lokalen " +
            "Debug-Signier-Fallback für Test-Builds zu verwenden.",
    )
}

val hasReleaseSigning = allSigningSet && releaseKeystoreFile != null && releaseKeystoreFile.isFile

android {
    namespace = "de.pytales.zdf"
    compileSdk = libs.versions.android.compileSdk.get().toInt()

    defaultConfig {
        applicationId = "de.pytales.zdf"
        minSdk = libs.versions.android.minSdk.get().toInt()
        targetSdk = libs.versions.android.targetSdk.get().toInt()
        versionCode = releaseVersionCode
        versionName = releaseVersionName
    }

    signingConfigs {
        if (hasReleaseSigning) {
            create("release") {
                storeFile = releaseKeystoreFile
                storePassword = releaseKeystorePassword
                keyAlias = releaseKeyAlias
                keyPassword = releaseKeyPassword
                enableV1Signing = true
                enableV2Signing = true
                enableV3Signing = true
            }
        }
    }

    buildTypes {
        debug {
            versionNameSuffix = "-debug"
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
            // Echte Release-Signierung falls Secrets gesetzt sind; sonst sauberer Fallback
            // auf Debug-Signierung (direkt installierbare Test-/Schul-APK) oder unsigniert
            // (wenn ZDF_UNSIGNED_RELEASE=true).
            signingConfig = when {
                hasReleaseSigning -> signingConfigs.getByName("release")
                allowUnsignedRelease -> null
                else -> signingConfigs.getByName("debug")
            }
        }
    }

    buildFeatures {
        compose = true
    }

    packaging {
        resources {
            excludes += "/META-INF/{AL2.0,LGPL2.1}"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
    }
}

dependencies {
    implementation(projects.composeApp)
    implementation(libs.androidx.activity.compose)
}
