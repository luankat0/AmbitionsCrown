import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from src.screens.campaign.regions.detail import RegionScreen
from src.ui.location.location_tree_view import LocationTreeView


class CampaignLocationHierarchyViewTests(unittest.TestCase):

    def test_region_loads_complete_location_hierarchy(self):
        city = SimpleNamespace(
            id=1,
            parent_location_id=None
        )

        castle = SimpleNamespace(
            id=2,
            parent_location_id=1
        )

        tower = SimpleNamespace(
            id=3,
            parent_location_id=2
        )

        repository = Mock()
        repository.get_all_by_region.return_value = [
            city,
            castle,
            tower
        ]

        screen = RegionScreen.__new__(RegionScreen)
        screen.region = SimpleNamespace(id=10)
        screen.app = SimpleNamespace(
            campaign_location_repository=repository
        )

        screen.refresh_locations()

        repository.get_all_by_region.assert_called_once_with(10)

        self.assertEqual(
            screen.locations,
            [city, castle, tower]
        )

        tree = LocationTreeView.__new__(LocationTreeView)

        roots, children = tree._build_tree(
            screen.locations
        )

        self.assertEqual(roots, [city])
        self.assertEqual(children[city.id], [castle])
        self.assertEqual(children[castle.id], [tower])


if __name__ == "__main__":
    unittest.main()

