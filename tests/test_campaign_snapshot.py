import unittest
from unittest.mock import patch

from src.core.database import Database

from src.domain.world.models.world import World
from src.domain.world.models.faction import Faction
from src.domain.world.models.region import Region
from src.domain.world.models.location import Location

from src.domain.world.repositories.world_repository import WorldRepository
from src.domain.world.repositories.region_repository import RegionRepository
from src.domain.world.repositories.location_repository import LocationRepository
from src.domain.world.repositories.faction_repository import FactionRepository

from src.domain.campaign.models.campaign import Campaign
from src.domain.campaign.models.campaign_faction import CampaignFaction

from src.domain.campaign.repositories.campaign_repository import CampaignRepository
from src.domain.campaign.repositories.campaign_region_repository import CampaignRegionRepository
from src.domain.campaign.repositories.campaign_location_repository import CampaignLocationRepository
from src.domain.campaign.repositories.campaign_faction_repository import CampaignFactionRepository

from src.domain.campaign.services.campaign_snapshot_service import CampaignSnapshotService


class CampaignSnapshotTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

        self.worlds = WorldRepository(self.database)
        self.regions = RegionRepository(self.database)
        self.locations = LocationRepository(self.database)
        self.factions = FactionRepository(self.database)

        self.campaigns = CampaignRepository(self.database)
        self.campaign_regions = CampaignRegionRepository(self.database)
        self.campaign_locations = CampaignLocationRepository(self.database)
        self.campaign_factions = CampaignFactionRepository(self.database)

        world = self.worlds.add(
            World(name="Mundo dos testes")
        )
        assert world.id is not None
        self.world_id: int = world.id

        self.campaign = self.campaigns.add(
            Campaign(
                name="Campanha teste",
                world_id=self.world_id
            )
        )
        assert self.campaign.id is not None
        self.campaign_id: int = self.campaign.id

        self.snapshot_service = CampaignSnapshotService(
            campaign_repository=self.campaigns,
            faction_repository=self.factions,
            campaign_faction_repository=self.campaign_factions,
            region_repository=self.regions,
            campaign_region_repository=self.campaign_regions,
            location_repository=self.locations,
            campaign_location_repository=self.campaign_locations,
        )

    def create_faction(self, name):
        faction = self.factions.add(
            Faction(
                world_id=self.world_id,
                name=name
            )
        )
        assert faction.id is not None
        return faction
    
    def prepare_world_for_rollback(self):
        region = self.regions.add(
            Region(
                world_id=self.world_id,
                name="Região de teste"
            )
        )
        assert region.id is not None

        location = self.locations.add(
            Location(
                region_id=region.id,
                name="Cidade de teste"
            )
        )
        assert location.id is not None

        self.create_faction("Alfa")
        self.create_faction("Zeta")


    def assert_snapshot_rolled_back(self):
        self.assertEqual(
            self.campaign_regions.get_all_by_campaign(
                self.campaign_id
            ),
            []
        )

        self.assertEqual(
            self.campaign_locations.get_all_by_campaign(
                self.campaign_id
            ),
            []
        )

        self.assertEqual(
            self.campaign_factions.get_all_by_campaign(
                self.campaign_id
            ),
            []
        )

        row = self.database.connection.execute(
            """
            SELECT snapshot_created_at
            FROM campaigns
            WHERE id = ?
            """,
            (self.campaign_id,)
        ).fetchone()

        assert row is not None

        self.assertIsNone(row["snapshot_created_at"])
        self.assertIsNone(
            self.campaign.snapshot_created_at
        )

    def test_initial_snapshot_copies_factions(self):
        alpha = self.create_faction("Alfa")
        zeta = self.create_faction("Zeta")

        result = self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        copied = self.campaign_factions.get_all_by_campaign(
            self.campaign_id
        )

        self.assertEqual(len(result["factions"]), 2)

        self.assertEqual(
            {f.source_faction_id for f in copied},
            {alpha.id, zeta.id}
        )

        self.assertIsNotNone(
            self.campaign.snapshot_created_at
        )

    def test_resume_partial_snapshot_without_duplicating_factions(self):
        alpha = self.create_faction("Alfa")
        zeta = self.create_faction("Zeta")

        # Simula uma facção já copiada antes da conclusão
        self.campaign_factions.add(
            CampaignFaction(
                campaign_id=self.campaign_id,
                source_faction_id=zeta.id,
                name="Zeta personalizada"
            )
        )

        result = self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        copied = self.campaign_factions.get_all_by_campaign(
            self.campaign_id
        )

        self.assertEqual(len(result["factions"]), 1)
        self.assertEqual(len(copied), 2)

        self.assertEqual(
            {f.source_faction_id for f in copied},
            {alpha.id, zeta.id}
        )

        preserved = next(
            f for f in copied
            if f.source_faction_id == zeta.id
        )

        self.assertEqual(
            preserved.name,
            "Zeta personalizada"
        )

        self.assertIsNotNone(
            self.campaign.snapshot_created_at
        )

    def test_reject_second_initial_snapshot(self):
        self.create_faction("Alfa")

        self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        with self.assertRaisesRegex(ValueError, "já possui"):
            self.snapshot_service.create_initial_snapshot(
                self.campaign
            )

        copied = self.campaign_factions.get_all_by_campaign(
            self.campaign_id
        )

        self.assertEqual(len(copied), 1)

    def test_rollback_when_faction_copy_fails(self):
        self.prepare_world_for_rollback()

        original_add = self.campaign_factions.add
        attempts = 0

        def fail_on_second_faction(faction, commit=True):
            nonlocal attempts

            attempts += 1

            if attempts == 2:
                raise RuntimeError(
                    "Falha simulada na segunda facção."
                )

            return original_add(
                faction,
                commit=commit
            )

        with patch.object(
            self.campaign_factions,
            "add",
            side_effect=fail_on_second_faction
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada"
            ):
                self.snapshot_service.create_initial_snapshot(
                    self.campaign
                )

        self.assertEqual(attempts, 2)

        self.assert_snapshot_rolled_back()

        # Após a falha, o snapshot deve poder ser refeito.
        result = self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        self.assertEqual(len(result["regions"]), 1)
        self.assertEqual(len(result["locations"]), 1)
        self.assertEqual(len(result["factions"]), 2)

        self.assertIsNotNone(
            self.campaign.snapshot_created_at
        )
    
    def test_rollback_when_snapshot_marker_fails(self):
        self.prepare_world_for_rollback()

        original_marker = (
            self.campaigns.mark_snapshot_created
        )

        def fail_after_marker(campaign, commit=True):
            original_marker(
                campaign,
                commit=commit
            )

            raise RuntimeError(
                "Falha simulada na finalização."
            )

        with patch.object(
            self.campaigns,
            "mark_snapshot_created",
            side_effect=fail_after_marker
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada"
            ):
                self.snapshot_service.create_initial_snapshot(
                    self.campaign
                )

        self.assert_snapshot_rolled_back()

        # O serviço deve continuar recuperável.
        result = self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        self.assertEqual(len(result["regions"]), 1)
        self.assertEqual(len(result["locations"]), 1)
        self.assertEqual(len(result["factions"]), 2)

        self.assertIsNotNone(
            self.campaign.snapshot_created_at
        )

if __name__ == "__main__":
    unittest.main()

