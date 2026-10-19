import unittest

from src.core.database import Database

from src.domain.campaign.models.campaign import Campaign
from src.domain.campaign.models.campaign_region import CampaignRegion
from src.domain.campaign.models.campaign_faction import CampaignFaction

from src.domain.campaign.repositories.campaign_repository import (
    CampaignRepository,
)
from src.domain.campaign.repositories.campaign_region_repository import (
    CampaignRegionRepository,
)
from src.domain.campaign.repositories.campaign_faction_repository import (
    CampaignFactionRepository,
)


class CampaignEntityOwnershipTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

        self.campaigns = CampaignRepository(self.database)
        self.regions = CampaignRegionRepository(self.database)
        self.factions = CampaignFactionRepository(self.database)

        campaign = self.campaigns.add(
            Campaign(name="Campanha de teste")
        )

        assert campaign.id is not None
        self.campaign_id: int = campaign.id

    def test_add_region_for_existing_campaign(self):
        region = self.regions.add(
            CampaignRegion(
                campaign_id=self.campaign_id,
                name="Reino"
            )
        )

        assert region.id is not None

        saved = self.regions.get_by_id(region.id)
        assert saved is not None

        self.assertEqual(
            saved.campaign_id,
            self.campaign_id
        )

    def test_add_faction_for_existing_campaign(self):
        faction = self.factions.add(
            CampaignFaction(
                campaign_id=self.campaign_id,
                name="Ordem Arcana"
            )
        )

        assert faction.id is not None

        saved = self.factions.get_by_id(faction.id)
        assert saved is not None

        self.assertEqual(
            saved.campaign_id,
            self.campaign_id
        )

    def test_reject_region_for_missing_campaign(self):
        with self.assertRaisesRegex(ValueError, "campanha"):
            self.regions.add(
                CampaignRegion(
                    campaign_id=999_999,
                    name="Região órfã"
                )
            )

        self.assertEqual(
            self.regions.get_all_by_campaign(999_999),
            []
        )

    def test_reject_faction_for_missing_campaign(self):
        with self.assertRaisesRegex(ValueError, "campanha"):
            self.factions.add(
                CampaignFaction(
                    campaign_id=999_999,
                    name="Facção órfã"
                )
            )

        self.assertEqual(
            self.factions.get_all_by_campaign(999_999),
            []
        )

    def test_historical_source_ids_need_not_exist(self):
        region = self.regions.add(
            CampaignRegion(
                campaign_id=self.campaign_id,
                source_region_id=999_998,
                name="Reino"
            )
        )

        faction = self.factions.add(
            CampaignFaction(
                campaign_id=self.campaign_id,
                source_faction_id=999_997,
                name="Ordem"
            )
        )

        assert region.id is not None
        assert faction.id is not None

        saved_region = self.regions.get_by_id(region.id)
        saved_faction = self.factions.get_by_id(faction.id)

        assert saved_region is not None
        assert saved_faction is not None

        self.assertEqual(
            saved_region.source_region_id,
            999_998
        )

        self.assertEqual(
            saved_faction.source_faction_id,
            999_997
        )

    def test_commit_false_keeps_rows_rollbackable(self):
        region = self.regions.add(
            CampaignRegion(
                campaign_id=self.campaign_id,
                name="Reino"
            ),
            commit=False
        )

        faction = self.factions.add(
            CampaignFaction(
                campaign_id=self.campaign_id,
                name="Ordem"
            ),
            commit=False
        )

        assert region.id is not None
        assert faction.id is not None

        self.database.connection.rollback()

        self.assertIsNone(
            self.regions.get_by_id(region.id)
        )

        self.assertIsNone(
            self.factions.get_by_id(faction.id)
        )

    def test_reject_faction_update_from_other_campaign(self):
        campaign_b = self.campaigns.add(
            Campaign(name="Campanha B")
        )

        assert campaign_b.id is not None

        faction_b = self.factions.add(
            CampaignFaction(
                campaign_id=campaign_b.id,
                name="Ordem da Campanha B"
            )
        )

        assert faction_b.id is not None

        # O objeto declara pertencer à Campaign A,
        # mas utiliza o ID da Facção da Campaign B.
        forged_faction = CampaignFaction(
            id=faction_b.id,
            campaign_id=self.campaign_id,
            name="Alteração indevida"
        )

        with self.assertRaisesRegex(
            ValueError,
            "campanha"
        ):
            self.factions.update(forged_faction)

        # A Facção original não deve ser modificada.
        saved = self.factions.get_by_id(
            faction_b.id
        )

        assert saved is not None

        self.assertEqual(
            saved.name,
            "Ordem da Campanha B"
        )

        self.assertEqual(
            saved.campaign_id,
            campaign_b.id
        )

    def test_reject_faction_delete_from_other_campaign(self):
        campaign_b = self.campaigns.add(
            Campaign(name="Campanha B")
        )

        assert campaign_b.id is not None

        faction_b = self.factions.add(
            CampaignFaction(
                campaign_id=campaign_b.id,
                name="Ordem da Campanha B"
            )
        )

        assert faction_b.id is not None

        # Declara pertencer à Campaign A,
        # mas utiliza o ID de uma Facção da Campaign B.
        forged_faction = CampaignFaction(
            id=faction_b.id,
            campaign_id=self.campaign_id,
            name="Ordem da Campanha B"
        )

        with self.assertRaisesRegex(
            ValueError,
            "campanha"
        ):
            self.factions.delete(forged_faction)

        # A Facção original deve continuar existindo.
        saved = self.factions.get_by_id(
            faction_b.id
        )

        assert saved is not None

        self.assertEqual(
            saved.name,
            "Ordem da Campanha B"
        )

        self.assertEqual(
            saved.campaign_id,
            campaign_b.id
        )

if __name__ == "__main__":
    unittest.main()

