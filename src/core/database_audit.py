import sqlite3


def find_orphan_region_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica Regions associadas a Worlds
    inexistentes.

    A operação é somente de leitura.
    Não modifica nem remove registros.
    """

    rows = connection.execute(
        """
        SELECT regions.id
        FROM regions
        LEFT JOIN worlds
            ON worlds.id = regions.world_id
        WHERE worlds.id IS NULL
        ORDER BY regions.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]
    
def find_orphan_location_region_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica Locations cujo region_id aponta
    para uma Region inexistente.

    Operação somente de leitura.
    Não altera nem exclui registros.
    """

    rows = connection.execute(
        """
        SELECT locations.id
        FROM locations
        LEFT JOIN regions
            ON regions.id = locations.region_id
        WHERE regions.id IS NULL
        ORDER BY locations.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_location_parent_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica Locations cujo parent_location_id
    aponta para uma Location inexistente.

    Locations raiz (parent_location_id NULL)
    não são consideradas órfãs.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT child.id
        FROM locations AS child
        LEFT JOIN locations AS parent
            ON parent.id = child.parent_location_id
        WHERE child.parent_location_id IS NOT NULL
          AND parent.id IS NULL
        ORDER BY child.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_location_parent_region_mismatch_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica Locations cujo pai pertence
    a uma Region diferente.

    Considera apenas pais existentes.
    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT child.id
        FROM locations AS child

        INNER JOIN locations AS parent
            ON parent.id = child.parent_location_id

        WHERE child.parent_location_id IS NOT NULL
          AND child.region_id != parent.region_id

        ORDER BY child.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_campaign_region_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica CampaignRegions associadas
    a Campaigns inexistentes.

    source_region_id é histórico e não
    participa dessa validação.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT cr.id
        FROM campaign_regions AS cr

        LEFT JOIN campaigns AS c
            ON c.id = cr.campaign_id

        WHERE c.id IS NULL

        ORDER BY cr.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_campaign_location_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica CampaignLocations associadas
    a Campaigns inexistentes.

    source_location_id é histórico e não
    participa dessa validação.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT cl.id
        FROM campaign_locations AS cl

        LEFT JOIN campaigns AS c
            ON c.id = cl.campaign_id

        WHERE c.id IS NULL

        ORDER BY cl.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_invalid_campaign_location_region_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica CampaignLocations cuja Region
    não existe ou pertence a outra Campaign.

    source_location_id é histórico e não
    participa desta validação.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT cl.id
        FROM campaign_locations AS cl

        LEFT JOIN campaign_regions AS cr
            ON cr.id = cl.region_id

        WHERE cr.id IS NULL
           OR cr.campaign_id != cl.campaign_id

        ORDER BY cl.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_campaign_location_parent_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica CampaignLocations cujo
    parent_location_id aponta para uma
    CampaignLocation inexistente.

    Locations raiz não são consideradas órfãs.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT child.id
        FROM campaign_locations AS child

        LEFT JOIN campaign_locations AS parent
            ON parent.id = child.parent_location_id

        WHERE child.parent_location_id IS NOT NULL
          AND parent.id IS NULL

        ORDER BY child.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_campaign_location_parent_mismatch_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica CampaignLocations cujo pai existe,
    mas pertence a outra Campaign ou Region.

    Pais inexistentes são tratados por outra
    auditoria.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT child.id
        FROM campaign_locations AS child

        INNER JOIN campaign_locations AS parent
            ON parent.id = child.parent_location_id

        WHERE child.campaign_id != parent.campaign_id
           OR child.region_id != parent.region_id

        ORDER BY child.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_campaign_faction_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica CampaignFactions associadas
    a Campaigns inexistentes.

    source_faction_id é uma referência histórica
    e não participa desta validação.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT cf.id
        FROM campaign_factions AS cf

        LEFT JOIN campaigns AS c
            ON c.id = cf.campaign_id

        WHERE c.id IS NULL

        ORDER BY cf.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_campaign_world_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica Campaigns associadas a
    Worlds inexistentes.

    Campaigns com world_id NULL são válidas.

    Operação somente de leitura.
    """

    rows = connection.execute(
        """
        SELECT c.id
        FROM campaigns AS c

        LEFT JOIN worlds AS w
            ON w.id = c.world_id

        WHERE c.world_id IS NOT NULL
          AND w.id IS NULL

        ORDER BY c.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def find_orphan_faction_world_ids(
    connection: sqlite3.Connection
) -> list[int]:
    """
    Identifica Factions canônicas associadas
    a Worlds inexistentes.

    Operação somente de leitura.
    Não modifica nem exclui registros.
    """

    rows = connection.execute(
        """
        SELECT f.id
        FROM factions AS f

        LEFT JOIN worlds AS w
            ON w.id = f.world_id

        WHERE w.id IS NULL

        ORDER BY f.id
        """
    ).fetchall()

    return [
        row[0]
        for row in rows
    ]

def audit_database_integrity(
    connection: sqlite3.Connection
) -> dict[str, list[int]]:
    """
    Executa todas as auditorias de integridade.

    Retorna um dicionário contendo os IDs
    inconsistentes, agrupados por categoria.

    Operação somente de leitura.
    """

    checks = {
        "regions_without_world":
            find_orphan_region_ids,

        "locations_without_region":
            find_orphan_location_region_ids,

        "locations_without_parent":
            find_orphan_location_parent_ids,

        "locations_parent_region_mismatch":
            find_location_parent_region_mismatch_ids,

        "campaign_regions_without_campaign":
            find_orphan_campaign_region_ids,

        "campaign_locations_without_campaign":
            find_orphan_campaign_location_ids,

        "campaign_locations_invalid_region":
            find_invalid_campaign_location_region_ids,

        "campaign_locations_without_parent":
            find_orphan_campaign_location_parent_ids,

        "campaign_locations_parent_mismatch":
            find_campaign_location_parent_mismatch_ids,

        "campaign_factions_without_campaign":
            find_orphan_campaign_faction_ids,

        "campaigns_without_world":
            find_orphan_campaign_world_ids,

        "factions_without_world":
            find_orphan_faction_world_ids,
    }

    return {
        name: check(connection)
        for name, check in checks.items()
    }

def validate_migration_integrity(
    connection: sqlite3.Connection
) -> None:
    """
    Valida as relações verificadas pelas
    auditorias antes de uma migração.

    Lança ValueError se encontrar problemas.

    Não altera registros nem executa migrations.
    """

    report = audit_database_integrity(
        connection
    )

    problems = {
        category: ids
        for category, ids in report.items()
        if ids
    }

    if not problems:
        return

    details = "; ".join(
        f"{category}: IDs {ids}"
        for category, ids in problems.items()
    )

    raise ValueError(
        "Migração bloqueada: foram encontradas "
        f"inconsistências no banco. {details}"
    )
