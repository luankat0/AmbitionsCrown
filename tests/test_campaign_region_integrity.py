import unittest

from src.core.database import Database

from src.domain.campaign.models.campaign import Campaign
from src.domain.campaign.models.campaign_region import CampaignRegion
from src.domain.campaign.models.campaign_location import CampaignLocation

from src.domain.campaign.repositories.campaign_repository import (
    CampaignRepository,
)
from src.domain.campaign.repositories.campaign_region_repository import (
    CampaignRegionRepository,
)
from src.domain.campaign.repositories.campaign_location_repository import (
    CampaignLocationRepository,
)


class CampaignRegionIntegrityTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

        self.campaigns = CampaignRepository(self.database)
        self.regions = CampaignRegionRepository(self.database)
        self.locations = CampaignLocationRepository(self.database)

        campaign = self.campaigns.add(
            Campaign(name="Campanha teste")
        )

        assert campaign.id is not None
        self.campaign_id: int = campaign.id

    def create_region(self, name="Região teste"):
        region = self.regions.add(
            CampaignRegion(
                campaign_id=self.campaign_id,
                name=name
            )
        )

        assert region.id is not None
        return region

    def test_delete_empty_campaign_region(self):
        region = self.create_region()

        self.regions.delete(region)

        self.assertIsNone(
            self.regions.get_by_id(region.id)
        )

    def test_reject_delete_region_with_locations(self):
        region = self.create_region()
        assert region.id is not None

        location = self.locations.add(
            CampaignLocation(
                campaign_id=self.campaign_id,
                region_id=region.id,
                name="Castelo"
            )
        )

        assert location.id is not None

        with self.assertRaisesRegex(ValueError, "locais"):
            self.regions.delete(region)

        self.assertIsNotNone(
            self.regions.get_by_id(region.id)
        )

        self.assertIsNotNone(
            self.locations.get_by_id(location.id)
        )

    def test_delete_empty_region_does_not_affect_other_region(self):
        occupied_region = self.create_region(
            "Região ocupada"
        )
        assert occupied_region.id is not None

        empty_region = self.create_region(
            "Região vazia"
        )

        location = self.locations.add(
            CampaignLocation(
                campaign_id=self.campaign_id,
                region_id=occupied_region.id,
                name="Cidade"
            )
        )

        assert location.id is not None

        self.regions.delete(empty_region)

        self.assertIsNone(
            self.regions.get_by_id(empty_region.id)
        )

        self.assertIsNotNone(
            self.regions.get_by_id(occupied_region.id)
        )

        self.assertIsNotNone(
            self.locations.get_by_id(location.id)
        )

    def test_reject_delete_region_without_id(self):
        region = CampaignRegion(
            campaign_id=self.campaign_id,
            name="Região não persistida"
        )

        with self.assertRaisesRegex(ValueError, "sem ID"):
            self.regions.delete(region)


if __name__ == "__main__":
    unittest.main()