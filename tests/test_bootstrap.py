import unittest

from src.core.database import Database
from src.core.bootstrap import build_dependencies


class BootstrapTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

    def test_all_repositories_share_the_same_database(self):
        dependencies = build_dependencies(self.database)

        repositories = (
            dependencies.npc_repository,
            dependencies.world_repository,
            dependencies.region_repository,
            dependencies.location_repository,
            dependencies.faction_repository,
            dependencies.campaign_repository,
            dependencies.campaign_region_repository,
            dependencies.campaign_location_repository,
            dependencies.campaign_faction_repository,
        )

        for repository in repositories:
            with self.subTest(repository=type(repository).__name__):
                self.assertIs(
                    repository.database,
                    self.database
                )

    def test_snapshot_service_uses_created_repositories(self):
        dependencies = build_dependencies(self.database)

        service = dependencies.campaign_snapshot_service

        self.assertIs(
            service.campaign_repository,
            dependencies.campaign_repository
        )

        self.assertIs(
            service.faction_repository,
            dependencies.faction_repository
        )

        self.assertIs(
            service.campaign_faction_repository,
            dependencies.campaign_faction_repository
        )

        self.assertIs(
            service.region_repository,
            dependencies.region_repository
        )

        self.assertIs(
            service.campaign_region_repository,
            dependencies.campaign_region_repository
        )

        self.assertIs(
            service.location_repository,
            dependencies.location_repository
        )

        self.assertIs(
            service.campaign_location_repository,
            dependencies.campaign_location_repository
        )


if __name__ == "__main__":
    unittest.main()

