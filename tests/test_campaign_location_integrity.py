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


class CampaignLocationIntegrityTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

        self.campaigns = CampaignRepository(self.database)
        self.regions = CampaignRegionRepository(self.database)
        self.locations = CampaignLocationRepository(self.database)

        campaign = self.campaigns.add(
            Campaign(name="Campanha A")
        )
        assert campaign.id is not None
        self.campaign_id: int = campaign.id

        region = self.regions.add(
            CampaignRegion(
                campaign_id=self.campaign_id,
                name="Região A"
            )
        )
        assert region.id is not None
        self.region_id: int = region.id

    def create_other_campaign_region(self):
        campaign = self.campaigns.add(
            Campaign(name="Campanha B")
        )
        assert campaign.id is not None

        region = self.regions.add(
            CampaignRegion(
                campaign_id=campaign.id,
                name="Região B"
            )
        )
        assert region.id is not None

        return campaign.id, region.id

    def test_create_root_location_in_valid_campaign(self):
        location = self.locations.add(
            CampaignLocation(
                campaign_id=self.campaign_id,
                region_id=self.region_id,
                name="Cidade"
            )
        )
        assert location.id is not None

        saved = self.locations.get_by_id(location.id)
        assert saved is not None

        self.assertEqual(saved.campaign_id, self.campaign_id)
        self.assertEqual(saved.region_id, self.region_id)
        self.assertIsNone(saved.parent_location_id)

    def test_create_child_in_same_campaign_and_region(self):
        parent = self.locations.add(
            CampaignLocation(
                campaign_id=self.campaign_id,
                region_id=self.region_id,
                name="Cidade"
            )
        )
        assert parent.id is not None

        child = self.locations.add(
            CampaignLocation(
                campaign_id=self.campaign_id,
                region_id=self.region_id,
                parent_location_id=parent.id,
                name="Castelo"
            )
        )
        assert child.id is not None

        self.assertEqual(child.parent_location_id, parent.id)
        self.assertEqual(
            len(self.locations.get_children(parent.id)),
            1
        )

    def test_reject_nonexistent_campaign(self):
        with self.assertRaisesRegex(ValueError, "campanha"):
            self.locations.add(
                CampaignLocation(
                    campaign_id=999_999,
                    region_id=self.region_id,
                    name="Local inválido"
                )
            )

        self.assertEqual(
            self.locations.get_all_by_campaign(self.campaign_id),
            []
        )

    def test_reject_nonexistent_region(self):
        with self.assertRaisesRegex(ValueError, "região"):
            self.locations.add(
                CampaignLocation(
                    campaign_id=self.campaign_id,
                    region_id=999_999,
                    name="Local inválido"
                )
            )

    def test_reject_region_from_another_campaign(self):
        _, other_region_id = (
            self.create_other_campaign_region()
        )

        with self.assertRaisesRegex(ValueError, "mesma campanha"):
            self.locations.add(
                CampaignLocation(
                    campaign_id=self.campaign_id,
                    region_id=other_region_id,
                    name="Local cruzado"
                )
            )

    def test_reject_parent_from_another_campaign(self):
        other_campaign_id, other_region_id = (
            self.create_other_campaign_region()
        )

        parent = self.locations.add(
            CampaignLocation(
                campaign_id=other_campaign_id,
                region_id=other_region_id,
                name="Cidade B"
            )
        )
        assert parent.id is not None

        with self.assertRaisesRegex(ValueError, "mesma campanha"):
            self.locations.add(
                CampaignLocation(
                    campaign_id=self.campaign_id,
                    region_id=self.region_id,
                    parent_location_id=parent.id,
                    name="Filho inválido"
                )
            )


if __name__ == "__main__":
    unittest.main()

