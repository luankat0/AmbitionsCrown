import unittest

from src.core.database import Database

from src.domain.world.models.world import World
from src.domain.world.repositories.world_repository import (
    WorldRepository,
)

from src.domain.campaign.models.campaign import (
    Campaign,
    CampaignStatus,
)
from src.domain.campaign.repositories.campaign_repository import (
    CampaignRepository,
)


class CampaignWorldIntegrityTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

        self.worlds = WorldRepository(self.database)
        self.campaigns = CampaignRepository(self.database)

        world_a = self.worlds.add(
            World(name="Mundo A")
        )
        world_b = self.worlds.add(
            World(name="Mundo B")
        )

        assert world_a.id is not None
        assert world_b.id is not None

        self.world_a_id: int = world_a.id
        self.world_b_id: int = world_b.id

        self.campaign = self.campaigns.add(
            Campaign(name="Campanha teste")
        )

        assert self.campaign.id is not None
        self.campaign_id: int = self.campaign.id

    def stored_campaign(self):
        row = self.database.connection.execute(
            """
            SELECT
                world_id,
                snapshot_created_at,
                name,
                description,
                status
            FROM campaigns
            WHERE id = ?
            """,
            (self.campaign_id,)
        ).fetchone()

        assert row is not None
        return row

    def complete_snapshot_marker(self):
        self.campaign.world_id = self.world_a_id

        self.campaigns.update(self.campaign)
        self.campaigns.mark_snapshot_created(
            self.campaign
        )

        assert self.campaign.snapshot_created_at is not None

    def test_assign_world_before_snapshot(self):
        self.campaign.world_id = self.world_a_id

        self.campaigns.update(self.campaign)

        saved = self.stored_campaign()

        self.assertEqual(
            saved["world_id"],
            self.world_a_id
        )
        self.assertIsNone(
            saved["snapshot_created_at"]
        )

    def test_reject_change_of_world_after_snapshot(self):
        self.complete_snapshot_marker()

        original_snapshot = (
            self.campaign.snapshot_created_at
        )

        self.campaign.world_id = self.world_b_id

        with self.assertRaisesRegex(ValueError, "mundo"):
            self.campaigns.update(self.campaign)

        saved = self.stored_campaign()

        self.assertEqual(
            saved["world_id"],
            self.world_a_id
        )
        self.assertEqual(
            saved["snapshot_created_at"],
            original_snapshot
        )

    def test_reject_manual_snapshot_timestamp(self):
        self.campaign.snapshot_created_at = (
            "2099-01-01 00:00:00"
        )

        with self.assertRaisesRegex(ValueError, "snapshot"):
            self.campaigns.update(self.campaign)

        self.assertIsNone(
            self.stored_campaign()["snapshot_created_at"]
        )

    def test_reject_removing_snapshot_timestamp(self):
        self.complete_snapshot_marker()

        original_snapshot = (
            self.campaign.snapshot_created_at
        )

        self.campaign.snapshot_created_at = None

        with self.assertRaisesRegex(ValueError, "snapshot"):
            self.campaigns.update(self.campaign)

        self.assertEqual(
            self.stored_campaign()["snapshot_created_at"],
            original_snapshot
        )

    def test_edit_narrative_fields_after_snapshot(self):
        self.complete_snapshot_marker()

        original_snapshot = (
            self.campaign.snapshot_created_at
        )

        self.campaign.name = "Campanha atualizada"
        self.campaign.description = "Descrição nova"
        self.campaign.status = CampaignStatus.ACTIVE

        self.campaigns.update(self.campaign)

        saved = self.stored_campaign()

        self.assertEqual(
            saved["name"],
            "Campanha atualizada"
        )
        self.assertEqual(
            saved["description"],
            "Descrição nova"
        )
        self.assertEqual(
            saved["status"],
            CampaignStatus.ACTIVE.value
        )
        self.assertEqual(
            saved["world_id"],
            self.world_a_id
        )
        self.assertEqual(
            saved["snapshot_created_at"],
            original_snapshot
        )

    def test_reject_creation_with_nonexistent_world(self):
        invalid_campaign = Campaign(
            name="Campanha inválida",
            world_id=999_999
        )

        with self.assertRaisesRegex(
            ValueError,
            "mundo"
        ):
            self.campaigns.add(invalid_campaign)

        # A Campaign inválida não deve ser persistida.
        row = self.database.connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM campaigns
            WHERE name = ?
            """,
            ("Campanha inválida",)
        ).fetchone()

        assert row is not None

        self.assertEqual(
            row["total"],
            0
        )

    def test_reject_update_with_nonexistent_world(self):
        # A Campaign ainda não possui World nem snapshot.
        self.assertIsNone(
            self.stored_campaign()["world_id"]
        )

        # Tenta associá-la a um World inexistente.
        self.campaign.world_id = 999_999

        with self.assertRaisesRegex(
            ValueError,
            "mundo"
        ):
            self.campaigns.update(self.campaign)

        # O banco deve preservar o estado anterior.
        saved = self.stored_campaign()

        self.assertIsNone(
            saved["world_id"]
        )

        self.assertIsNone(
            saved["snapshot_created_at"]
        )

if __name__ == "__main__":
    unittest.main()
    
