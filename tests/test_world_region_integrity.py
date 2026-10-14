import unittest

from src.core.database import Database
from src.domain.world.models.region import Region
from src.domain.world.models.faction import Faction
from src.domain.world.models.world import World
from src.domain.world.repositories.region_repository import RegionRepository
from src.domain.world.repositories.faction_repository import FactionRepository
from src.domain.world.repositories.world_repository import WorldRepository


class WorldRegionIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.database = Database(':memory:')
        self.addCleanup(self.database.close)
        self.database.create_tables()
        self.worlds = WorldRepository(self.database)
        self.regions = RegionRepository(self.database)
        self.factions = FactionRepository(self.database)

    def test_create_region_in_existing_world(self):
        world = self.worlds.add(World(name='Mundo de teste'))
        region = self.regions.add(
            Region(world_id=world.id, name='Região válida')
        )

        self.assertIsNotNone(region.id)
        saved = self.regions.get_by_id(region.id)
        self.assertIsNotNone(saved)
        self.assertEqual(saved.world_id, world.id)
        self.assertEqual(saved.name, 'Região válida')

    def test_reject_region_when_world_does_not_exist(self):
        region = Region(world_id=999_999, name='Região órfã')

        with self.assertRaisesRegex(ValueError, 'mundo'):
            self.regions.add(region)

        count = self.database.connection.execute(
            'SELECT COUNT(*) FROM regions'
        ).fetchone()[0]
        self.assertEqual(count, 0)

    def test_reject_world_deletion_when_it_has_regions(self):
        world = self.worlds.add(World(name='Mundo com região'))
        self.regions.add(Region(world_id=world.id, name='Região filha'))

        with self.assertRaisesRegex(ValueError, 'regiões'):
            self.worlds.delete(world)

        self.assertIsNotNone(self.worlds.get_by_id(world.id))

    def test_reject_world_deletion_when_it_has_factions(self):
        world = self.worlds.add(World(name='Mundo com facção'))
        self.factions.add(Faction(world_id=world.id, name='Facção filha'))

        with self.assertRaisesRegex(ValueError, 'facções'):
            self.worlds.delete(world)

        self.assertIsNotNone(self.worlds.get_by_id(world.id))


if __name__ == '__main__':
    unittest.main()
