from src.models.region import RegionType


REGION_TYPE_LABELS = {
    RegionType.KINGDOM: "Reino",
    RegionType.PROVINCE: "Província",
    RegionType.TERRITORY: "Território",
    RegionType.FOREST: "Floresta",
    RegionType.DESERT: "Deserto",
    RegionType.MOUNTAINS: "Montanhas",
    RegionType.ISLAND: "Ilha",
    RegionType.OTHER: "Outro",
}


def get_region_type_label(
    region_type: RegionType
):
    return REGION_TYPE_LABELS.get(
        region_type,
        region_type.value
    )