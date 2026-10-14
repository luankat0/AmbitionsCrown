def ensure_campaign_exists(
    database,
    campaign_id: int
) -> None:
    cursor = database.connection.execute(
        """ 
        SELECT 1
        FROM campaigns
        WHERE id = ?
        LIMIT 1
        """,
        (campaign_id,)
    )
    
    if cursor.fetchone() is None:
        raise ValueError(
            "A campanha informada não existe."
        )