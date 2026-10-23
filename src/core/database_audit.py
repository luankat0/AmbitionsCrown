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

