import unittest

from src.core.database import Database
from src.domain.world.models.world import World
from src.domain.world.models.region import Region
from src.domain.world.models.location import Location

from src.domain.world.repositories.world_repository import (
    WorldRepository,
)
from src.domain.world.repositories.region_repository import (
    RegionRepository,
)
from src.domain.world.repositories.location_repository import (
    LocationRepository,
)

class WorldLocationIntegrityTests(unittest.TestCase):
    
    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)
        self.database.create_tables()
        
        self.worlds = WorldRepository(self.database)
        self.regions = RegionRepository(self.database)
        self.locations = LocationRepository(self.database)
        
        world = self.worlds.add(
            World(name="Mundo de teste")
        )
        
        assert world.id is not None
        
        self.region = self.regions.add(
            Region(
                world_id=world.id,
                name="Região principal"
            )
        )
        
        assert self.region.id is not None
        
        self.region_id: int = self.region.id
        
    def test_create_root_location_in_existing_region(self):
        location = self.locations.add(
            Location(
                region_id=self.region_id,
                name="Cidade"
            )
        )
        
        assert location.id is not None
        
        saved = self.locations.get_by_id(location.id)
        
        assert saved is not None
        
        self.assertEqual(
            saved.region_id,
            self.region_id
        )
        
        self.assertIsNone(
            saved.parent_location_id
        )
        
    def test_reject_location_when_region_does_not_exist(self):
        with self.assertRaisesRegex(ValueError, "região"):
            self.locations.add(
                Location(
                    region_id=999_999,
                    name="Local órfão"
                )
            )
            
        count = self.database.connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0]
        
        self.assertEqual(count, 0)
        
    def test_create_child_location_in_same_region(self):
        parent = self.locations.add(
            Location(
                region_id=self.region_id,
                name="Cidade"
            )
        )
        
        assert parent.id is not None
        
        child = self.locations.add(
            Location(
                region_id=self.region_id,
                name="Castelo",
                parent_location_id=parent.id
            )
        )
        
        self.assertEqual(
            child.parent_location_id,
            parent.id
        )
        
        self.assertEqual(
            len(self.locations.get_children(parent.id)),
            1
        )
    
    def test_reject_nonexistent_parent(self):
        with self.assertRaisesRegex(ValueError, "pai"):
            self.locations.add(
                Location(
                    region_id=self.region_id,
                    name="Local",
                    parent_location_id=999_999
                )
            )
            
    def test_reject_parent_from_another_region(self):
        other_region = self.regions.add(
            Region(
                world_id=self.region.world_id,
                name="Outra região"
            )
        )
        
        assert other_region.id is not None
        
        parent = self.locations.add(
            Location(
                region_id=other_region.id,
                name="Outra cidade"
            )
        )
        
        with self.assertRaisesRegex(ValueError, "mesma região"):
            self.locations.add(
                Location(
                    region_id=self.region_id,
                    name="Filho inválido",
                    parent_location_id=parent.id
                )
            )
            
    def test_reject_deletion_of_location_with_children(self):
        parent = self.locations.add(
            Location(
                region_id=self.region_id,
                name="Cidade"
            )
        )
        
        assert parent.id is not None
        
        self.locations.add(
            Location(
                region_id=self.region_id,
                name="Castelo",
                parent_location_id=parent.id
            )
        )
        
        with self.assertRaisesRegex(ValueError, "sublocais"):
            self.locations.delete(parent)
            
        self.assertIsNotNone(
            self.locations.get_by_id(parent.id)
        )

    def test_reject_update_of_nonexistent_location(self):
        # Cria uma Location válida para garantir
        # que outros registros sejam preservados.
        valid_location = self.locations.add(
            Location(
                region_id=self.region_id,
                name="Cidade existente"
            )
        )

        assert valid_location.id is not None

        # Esta Location possui um ID inexistente.
        nonexistent_location = Location(
            id=999_999,
            region_id=self.region_id,
            name="Cidade inexistente"
        )

        with self.assertRaisesRegex(
            ValueError,
            "não existe"
        ):
            self.locations.update(nonexistent_location)

        # Confirma que a Location inexistente
        # não foi criada.
        self.assertIsNone(
            self.locations.get_by_id(
                nonexistent_location.id
            )
        )

        # Confirma que o registro válido
        # permanece intacto.
        saved = self.locations.get_by_id(
            valid_location.id
        )

        assert saved is not None

        self.assertEqual(
            saved.name,
            "Cidade existente"
        )

        self.assertEqual(
            saved.region_id,
            self.region_id
        )

    def test_reject_delete_of_nonexistent_location(self):
        # Cria uma Location válida.
        valid_location = self.locations.add(
            Location(
                region_id=self.region_id,
                name="Cidade existente"
            )
        )

        assert valid_location.id is not None

        # Esta Location possui um ID inexistente.
        nonexistent_location = Location(
            id=999_999,
            region_id=self.region_id,
            name="Cidade inexistente"
        )

        with self.assertRaisesRegex(
            ValueError,
            "não existe"
        ):
            self.locations.delete(nonexistent_location)

        # A Location válida deve continuar intacta.
        saved = self.locations.get_by_id(
            valid_location.id
        )

        assert saved is not None

        self.assertEqual(
            saved.name,
            "Cidade existente"
        )

        self.assertEqual(
            saved.region_id,
            self.region_id
        )

        # Nenhum registro deve existir com o ID inválido.
        self.assertIsNone(
            self.locations.get_by_id(
                nonexistent_location.id
            )
        )

if __name__ == "__main__":
    unittest.main()