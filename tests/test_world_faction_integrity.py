import unittest

from src.core.database import Database

from src.domain.world.models.world import World
from src.domain.world.models.faction import (
    Faction,
    FactionStatus,
    FactionType,
)

from src.domain.world.repositories.world_repository import (
    WorldRepository,
)

from src.domain.world.repositories.faction_repository import (
    FactionRepository,
)


class WorldFactionIntegrityTests(unittest.TestCase):
    
    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()

        self.worlds = WorldRepository(self.database)
        self.factions = FactionRepository(self.database)
        
        world = self.worlds.add(
            World(name="Mundo de teste")
        )
        assert world.id is not None
        
        self.world_id: int = world.id
        
    def test_create_faction_in_existing_world(self):
        faction = self.factions.add(
            Faction(
                world_id=self.world_id,
                name="Ordem Arcana"
            )
        )
        assert faction.id is not None
        
        saved = self.factions.get_by_id(
            faction.id
        )
        assert saved is not None
        
        self.assertEqual(
            saved.world_id,
            self.world_id
        )
        
        self.assertEqual(
            saved.name,
            "Ordem Arcana"
        )
        
        self.assertEqual(
            saved.faction_type,
            FactionType.OTHER
        )
        
        self.assertEqual(
            saved.status,
            FactionStatus.ACTIVE
        )
    
    def test_reject_faction_when_world_does_not_exist(self):
        with self.assertRaisesRegex(ValueError, "mundo"):
            self.factions.add(
                Faction(
                    world_id=999_999,
                    name="Facção órfã"
                )
            )
        
        count = self.database.connection.execute(
            "SELECT COUNT(*) FROM factions"
        ).fetchone()[0]
        
        self.assertEqual(count, 0)
    
    def test_update_faction_preserves_ownership(self):
        faction = self.factions.add(
            Faction(
                world_id=self.world_id,
                name="Nome original"
            )
        )
        assert faction.id is not None
        
        faction.name = "Nome atualizado"
        faction.status = FactionStatus.HIDDEN
        faction.description = "Descrição editada"
        
        self.factions.update(faction)
        
        saved = self.factions.get_by_id(
            faction.id
        )
        assert saved is not None
        
        self.assertEqual(
            saved.world_id,
            self.world_id
        )
        
        self.assertEqual(
            saved.name,
            "Nome atualizado"
        )
        
        self.assertEqual(
            saved.status,
            FactionStatus.HIDDEN
        )
        
        self.assertEqual(
            saved.description,
            "Descrição editada"
        )
    
    def test_delete_faction(self):
        faction = self.factions.add(
            Faction(
                world_id=self.world_id,
                name="Facção temporária"
            )
        )
        assert faction.id is not None
        
        self.factions.delete(faction)
        
        self.assertIsNone(
            self.factions.get_by_id(faction.id)
        )
        
        self.assertIsNotNone(
            self.worlds.get_by_id(self.world_id)
        )

    def test_reject_update_of_nonexistent_faction(self):
        faction = Faction(
            world_id=self.world_id,
            name="Facção inexistente",
            id=999_999
        )

        with self.assertRaisesRegex(
            ValueError,
            "não existe"
        ):
            self.factions.update(faction)

        self.assertIsNone(
            self.factions.get_by_id(faction.id)
        )

    def test_reject_delete_of_nonexistent_faction(self):
        faction = Faction(
            world_id=self.world_id,
            name="Facção inexistente",
            id=999_999
        )

        with self.assertRaisesRegex(
            ValueError,
            "não existe"
        ):
            self.factions.delete(faction)

if __name__ == "__main__":
    unittest.main()
        