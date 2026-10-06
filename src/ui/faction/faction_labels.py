from src.models.faction import (
    FactionStatus,
    FactionType
)

FACTION_TYPE_LABELS = {
    FactionType.KINGDOM: "Reino",
    FactionType.GOVERNMENT: "Governo",
    FactionType.GUILD: "Guilda",
    FactionType.RELIGION: "Organização Religiosa",
    FactionType.MILITARY: "Organização Militar",
    FactionType.CRIMINAL: "Organização Criminosa",
    FactionType.MERCHANT: "Organização Mercantil",
    FactionType.SECRET_SOCIETY: "Sociedade Secreta",
    FactionType.CULT: "Culto",
    FactionType.TRIBE: "Tribo",
    FactionType.OTHER: "Outro",
}

FACTION_STATUS_LABELS = {
    FactionStatus.ACTIVE: "Ativa",
    FactionStatus.INACTIVE: "Inativa",
    FactionStatus.DESTROYED: "Destruída",
    FactionStatus.HIDDEN: "Oculta",
}

def get_faction_type_label(
    faction_type: FactionType
) -> str:
    return (
        FACTION_TYPE_LABELS.get(
            faction_type
        ) 
        or faction_type.value
    )
    
def get_faction_status_label(
    faction_status: FactionStatus
) -> str:
    return (
        FACTION_STATUS_LABELS.get(
            faction_status
        )
        or faction_status.value
    )