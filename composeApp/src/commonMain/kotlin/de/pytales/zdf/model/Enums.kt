package de.pytales.zdf.model

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
enum class WertSchluessel(val code: String) {
    @SerialName("versorgung")
    VERSORGUNG("versorgung"),

    @SerialName("belastung")
    BELASTUNG("belastung"),

    @SerialName("aufmerksamkeit")
    AUFMERKSAMKEIT("aufmerksamkeit"),

    @SerialName("rueckhalt")
    RUECKHALT("rueckhalt"),
}

@Serializable
enum class Pfad(val code: String) {
    @SerialName("front")
    FRONT("front"),

    @SerialName("etappe")
    ETAPPE("etappe"),

    @SerialName("heimat")
    HEIMAT("heimat"),
}

@Serializable
enum class Stimmung(val code: String) {
    @SerialName("neutral")
    NEUTRAL("neutral"),

    @SerialName("hungrig")
    HUNGRIG("hungrig"),

    @SerialName("erschoepft")
    ERSCHOEPFT("erschoepft"),

    @SerialName("angst")
    ANGST("angst"),

    @SerialName("einsam")
    EINSAM("einsam"),
}

@Serializable
enum class SpielModus(val code: String) {
    @SerialName("kurz")
    KURZ("kurz"),

    @SerialName("lang")
    LANG("lang"),
}

@Serializable
enum class Geschlecht(val code: String) {
    @SerialName("m")
    MAENNLICH("m"),

    @SerialName("w")
    WEIBLICH("w"),
}

@Serializable
enum class Kartentyp(val code: String) {
    @SerialName("karte")
    KARTE("karte"),

    @SerialName("feldpost")
    FELDPOST("feldpost"),

    @SerialName("lebensmittel")
    LEBENSMITTEL("lebensmittel"),

    @SerialName("zeitung")
    ZEITUNG("zeitung"),

    @SerialName("amtlich")
    AMTLICH("amtlich"),
}

@Serializable
enum class EreignisKategorie(val code: String) {
    @SerialName("alltag")
    ALLTAG("alltag"),

    @SerialName("einstieg")
    EINSTIEG("einstieg"),

    @SerialName("finale")
    FINALE("finale"),

    @SerialName("kette")
    KETTE("kette"),
}

@Serializable
enum class HartesEndeId(val code: String) {
    @SerialName("ende_verhungert")
    ENDE_VERHUNGERT("ende_verhungert"),

    @SerialName("ende_zusammenbruch")
    ENDE_ZUSAMMENBRUCH("ende_zusammenbruch"),

    @SerialName("ende_verhaftet")
    ENDE_VERHAFTET("ende_verhaftet"),

    @SerialName("ende_gefallen")
    ENDE_GEFALLEN("ende_gefallen"),
}

@Serializable
enum class MusterungsGrad(val code: String) {
    @SerialName("kv")
    KV("kv"),

    @SerialName("gv")
    GV("gv"),

    @SerialName("av")
    AV("av"),

    @SerialName("du")
    DU("du"),
}

@Serializable
enum class MusterungsVermerk(val code: String) {
    @SerialName("uk")
    UK("uk"),

    @SerialName("zurueck")
    ZURUECK("zurueck"),
}

@Serializable
enum class MerkmalGruppe(val code: String) {
    @SerialName("tat")
    TAT("tat"),

    @SerialName("haltung")
    HALTUNG("haltung"),

    @SerialName("stellung")
    STELLUNG("stellung"),

    @SerialName("erwerb")
    ERWERB("erwerb"),

    @SerialName("herkunft")
    HERKUNFT("herkunft"),

    @SerialName("lage")
    LAGE("lage"),
}
