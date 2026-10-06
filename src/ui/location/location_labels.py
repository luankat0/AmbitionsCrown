from src.domain.world.models.location import LocationType


LOCATION_TYPE_LABELS = {
    LocationType.CITY: "Cidade",
    LocationType.VILLAGE: "Vila",
    LocationType.CAPITAL: "Capital",
    LocationType.DISTRICT: "Distrito",
    LocationType.FORTRESS: "Fortaleza",
    LocationType.CASTLE: "Castelo",
    LocationType.TOWER: "Torre",
    LocationType.DUNGEON: "Masmorra",
    LocationType.TEMPLE: "Templo",
    LocationType.RUIN: "Ruína",
    LocationType.TAVERN: "Taverna",
    LocationType.CAMP: "Acampamento",
    LocationType.LANDMARK: "Ponto de Interesse",
    LocationType.OTHER: "Outro",
}


def get_location_type_label(
    location_type: LocationType
):
    return LOCATION_TYPE_LABELS.get(
        location_type,
        location_type.value
    )