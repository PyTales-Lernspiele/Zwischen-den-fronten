# ==============================================================================
# R8 / ProGuard-Regeln für „Zwischen den Fronten“ (Android Release-Build)
# ==============================================================================

# Hilfreiche Stacktraces bei Fehlerberichten bewahren
-keepattributes SourceFile,LineNumberTable,*Annotation*,Signature,InnerClasses,EnclosingMethod
-renamesourcefileattribute SourceFile

# ------------------------------------------------------------------------------
# 1. kotlinx.serialization — alle JSON-Spielinhaltsmodelle unter de.pytales.zdf.model
# ------------------------------------------------------------------------------
-dontnote kotlinx.serialization.AnnotationsKt

-keep,includedescriptorclasses class de.pytales.zdf.model.** { *; }
-keepclassmembers class de.pytales.zdf.model.** {
    *** Companion;
}
-keepclasseswithmembers class de.pytales.zdf.model.** {
    kotlinx.serialization.KSerializer serializer(...);
}
-keepclassmembers class de.pytales.zdf.model.**$Companion {
    kotlinx.serialization.KSerializer serializer(...);
}
-keep class de.pytales.zdf.model.**$*serializer { *; }

# Allgemeine kotlinx.serialization-Regeln (Enums mit @SerialName, Companion, Serializer)
-keep,includedescriptorclasses class kotlinx.serialization.** { *; }
-keepclasseswithmembers class * {
    @kotlinx.serialization.Serializable <fields>;
}
-keepclassmembers class * {
    @kotlinx.serialization.SerialName <fields>;
}
-if @kotlinx.serialization.Serializable class **
-keepclassmembers class <1> {
    static <1>$Companion Companion;
}
-if @kotlinx.serialization.Serializable class **
-keepclasseswithmembers class <1>$Companion {
    kotlinx.serialization.KSerializer serializer(...);
}
-if @kotlinx.serialization.Serializable class **
-keep class <1>$$serializer { *; }

# ------------------------------------------------------------------------------
# 2. Compose Multiplatform Resources (content/*.json & content/media/**/*.webp)
# ------------------------------------------------------------------------------
-keep class de.pytales.zdf.resources.** { *; }
-keep class org.jetbrains.compose.resources.** { *; }
