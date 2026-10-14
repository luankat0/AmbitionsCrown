import unittest
import pygame

from src.ui.region.region_form import RegionForm
from src.ui.location.location_form import LocationForm

from src.domain.world.models.region import RegionType
from src.domain.world.models.location import LocationType

from src.domain.campaign.models.campaign_region import (
    CampaignRegion,
)
from src.domain.campaign.models.campaign_location import (
    CampaignLocation,
)


class CampaignFormValidationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.font_was_initialized = pygame.font.get_init()

        if not cls.font_was_initialized:
            pygame.font.init()

    @classmethod
    def tearDownClass(cls):
        if not cls.font_was_initialized:
            pygame.font.quit()

        super().tearDownClass()

    def test_region_requires_name_on_create_and_edit(self):
        for mode in ("create", "edit"):
            with self.subTest(mode=mode):
                form = RegionForm()

                if mode == "create":
                    form.prepare_create()
                else:
                    form.prepare_edit(
                        CampaignRegion(
                            campaign_id=1,
                            name="Região existente"
                        )
                    )

                form.name_input.text = "   "

                region = form.build_campaign_region(
                    campaign_id=1
                )

                self.assertIsNone(region)
                self.assertTrue(form.name_input.error)
                self.assertEqual(
                    form.validation_message,
                    "O nome da região é obrigatório."
                )

    def test_region_builds_valid_campaign_region(self):
        form = RegionForm()
        form.prepare_create()

        form.name_input.text = "  Reino do Norte  "
        form.description_input.text = " Descrição "
        form.notes_input.text = " Notas "

        form.region_type_index = (
            form.region_types.index(RegionType.KINGDOM)
        )

        region = form.build_campaign_region(
            campaign_id=7
        )

        assert region is not None

        self.assertEqual(region.campaign_id, 7)
        self.assertEqual(region.name, "Reino do Norte")
        self.assertEqual(region.region_type, RegionType.KINGDOM)
        self.assertEqual(region.description, "Descrição")
        self.assertEqual(region.notes, "Notas")

    def test_location_requires_name_on_create_and_edit(self):
        for mode in ("create", "edit"):
            with self.subTest(mode=mode):
                form = LocationForm()

                if mode == "create":
                    form.prepare_create()
                else:
                    form.prepare_edit(
                        CampaignLocation(
                            campaign_id=1,
                            region_id=2,
                            name="Local existente"
                        )
                    )

                form.name_input.text = "   "

                location = form.build_campaign_location(
                    campaign_id=1,
                    region_id=2
                )

                self.assertIsNone(location)
                self.assertTrue(form.name_input.error)
                self.assertEqual(
                    form.validation_message,
                    "O nome do local é obrigatório."
                )

    def test_location_builds_valid_campaign_location(self):
        form = LocationForm()
        form.prepare_create()

        form.name_input.text = "  Torre do Mago  "
        form.description_input.text = " Torre antiga "
        form.notes_input.text = " Segredo do mestre "

        form.location_type_index = (
            form.location_types.index(LocationType.TOWER)
        )

        location = form.build_campaign_location(
            campaign_id=7,
            region_id=3,
            parent_location_id=12
        )

        assert location is not None

        self.assertEqual(location.campaign_id, 7)
        self.assertEqual(location.region_id, 3)
        self.assertEqual(location.parent_location_id, 12)
        self.assertEqual(location.name, "Torre do Mago")
        self.assertEqual(location.location_type, LocationType.TOWER)
        self.assertEqual(location.description, "Torre antiga")
        self.assertEqual(location.notes, "Segredo do mestre")


if __name__ == "__main__":
    unittest.main()

