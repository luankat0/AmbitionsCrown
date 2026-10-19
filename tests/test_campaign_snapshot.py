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
from src.domain.campaign.models.campaign_location import CampaignLocation
from src.domain.campaign.models.campaign_region import CampaignRegion

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
    
    def create_world_hierarchy(self):
        region = self.regions.add(
            Region(
                world_id=self.world_id,
                name="Reino"
            )
        )

        assert region.id is not None

        city = self.locations.add(
            Location(
                region_id=region.id,
                name="Cidade"
            )
        )

        assert city.id is not None

        castle = self.locations.add(
            Location(
                region_id=region.id,
                parent_location_id=city.id,
                name="Castelo"
            )
        )

        assert castle.id is not None

        tower = self.locations.add(
            Location(
                region_id=region.id,
                parent_location_id=castle.id,
                name="Torre"
            )
        )

        assert tower.id is not None

        return (
            region.id,
            city.id,
            castle.id,
            tower.id
        )
    
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

    def test_snapshot_preserves_location_hierarchy(self):
        (
            region_id,
            city_id,
            castle_id,
            tower_id
        ) = self.create_world_hierarchy()

        # Cria conteúdo próprio antes do snapshot.
        # Isso também diferencia os IDs das duas tabelas.
        own_region = self.campaign_regions.add(
            CampaignRegion(
                campaign_id=self.campaign_id,
                name="Região própria"
            )
        )

        assert own_region.id is not None

        own_location = self.campaign_locations.add(
            CampaignLocation(
                campaign_id=self.campaign_id,
                region_id=own_region.id,
                name="Local próprio"
            )
        )

        assert own_location.id is not None

        result = self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        self.assertEqual(len(result["regions"]), 1)
        self.assertEqual(len(result["locations"]), 3)

        regions = self.campaign_regions.get_all_by_campaign(
            self.campaign_id
        )

        copied_region = next(
            region
            for region in regions
            if region.source_region_id == region_id
        )

        assert copied_region.id is not None

        # IDs próprios da Campaign.
        self.assertNotEqual(
            copied_region.id,
            region_id
        )

        locations = self.campaign_locations.get_all_by_campaign(
            self.campaign_id
        )

        copied = {
            location.source_location_id: location
            for location in locations
            if location.source_location_id is not None
        }

        self.assertEqual(
            set(copied),
            {city_id, castle_id, tower_id}
        )

        # Cidade é a raiz.
        self.assertIsNone(
            copied[city_id].parent_location_id
        )

        # Castelo pertence à Cidade copiada.
        self.assertEqual(
            copied[castle_id].parent_location_id,
            copied[city_id].id
        )

        # Torre pertence ao Castelo copiado.
        self.assertEqual(
            copied[tower_id].parent_location_id,
            copied[castle_id].id
        )

        # Todos pertencem à Region copiada.
        for location in copied.values():
            self.assertEqual(
                location.region_id,
                copied_region.id
            )

        # O local criado pela Campaign foi preservado.
        self.assertIn(
            own_location.id,
            {location.id for location in locations}
        )

    def test_campaign_snapshots_are_independent(self):
        (
            region_id,
            _,
            _,
            tower_id
        ) = self.create_world_hierarchy()

        campaign_b = self.campaigns.add(
            Campaign(
                name="Campanha B",
                world_id=self.world_id
            )
        )

        assert campaign_b.id is not None

        self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        self.snapshot_service.create_initial_snapshot(
            campaign_b
        )

        # Recupera as cópias de cada Campaign.
        region_a = next(
            region
            for region in self.campaign_regions.get_all_by_campaign(
                self.campaign_id
            )
            if region.source_region_id == region_id
        )

        region_b = next(
            region
            for region in self.campaign_regions.get_all_by_campaign(
                campaign_b.id
            )
            if region.source_region_id == region_id
        )

        tower_a = next(
            location
            for location in self.campaign_locations.get_all_by_campaign(
                self.campaign_id
            )
            if location.source_location_id == tower_id
        )

        tower_b = next(
            location
            for location in self.campaign_locations.get_all_by_campaign(
                campaign_b.id
            )
            if location.source_location_id == tower_id
        )

        assert region_a.id is not None
        assert region_b.id is not None
        assert tower_a.id is not None
        assert tower_b.id is not None

        # As cópias possuem identidades independentes.
        self.assertNotEqual(region_a.id, region_b.id)
        self.assertNotEqual(tower_a.id, tower_b.id)

        # Modifica somente a Campaign A.
        region_a.name = "Reino destruído"
        tower_a.name = "Torre abandonada"

        self.campaign_regions.update(region_a)
        self.campaign_locations.update(tower_a)

        # Modifica também o World original.
        world_region = self.regions.get_by_id(region_id)
        world_tower = self.locations.get_by_id(tower_id)

        assert world_region is not None
        assert world_tower is not None

        world_region.name = "Reino renovado"
        world_tower.name = "Torre restaurada"

        self.regions.update(world_region)
        self.locations.update(world_tower)

        # Reconsulta o banco para verificar persistência.
        saved_region_a = self.campaign_regions.get_by_id(
            region_a.id
        )
        saved_region_b = self.campaign_regions.get_by_id(
            region_b.id
        )

        saved_tower_a = self.campaign_locations.get_by_id(
            tower_a.id
        )
        saved_tower_b = self.campaign_locations.get_by_id(
            tower_b.id
        )

        assert saved_region_a is not None
        assert saved_region_b is not None
        assert saved_tower_a is not None
        assert saved_tower_b is not None

        self.assertEqual(
            saved_region_a.name,
            "Reino destruído"
        )
        self.assertEqual(
            saved_tower_a.name,
            "Torre abandonada"
        )

        self.assertEqual(saved_region_b.name, "Reino")
        self.assertEqual(saved_tower_b.name, "Torre")

        self.assertEqual(
            self.regions.get_by_id(region_id).name,
            "Reino renovado"
        )
        self.assertEqual(
            self.locations.get_by_id(tower_id).name,
            "Torre restaurada"
        )

    def test_reject_snapshot_with_stale_campaign(self):
        original_region = self.regions.add(
            Region(
                world_id=self.world_id,
                name="Região original"
            )
        )

        assert original_region.id is not None

        # Carrega uma instância antes da inicialização.
        stale_campaign = next(
            campaign
            for campaign in self.campaigns.get_all()
            if campaign.id == self.campaign_id
        )

        self.assertIsNone(
            stale_campaign.snapshot_created_at
        )

        # Conclui o snapshot com a instância principal.
        self.snapshot_service.create_initial_snapshot(
            self.campaign
        )

        self.assertIsNotNone(
            self.campaign.snapshot_created_at
        )

        # O objeto antigo continua desatualizado.
        self.assertIsNone(
            stale_campaign.snapshot_created_at
        )

        # Modificação posterior no World canônico.
        self.regions.add(
            Region(
                world_id=self.world_id,
                name="Região criada depois"
            )
        )

        # A tentativa de repetir o snapshot deve falhar.
        with self.assertRaisesRegex(
            ValueError,
            "já possui"
        ):
            self.snapshot_service.create_initial_snapshot(
                stale_campaign
            )

        # Apenas a Region original deve estar na Campaign.
        copied = self.campaign_regions.get_all_by_campaign(
            self.campaign_id
        )

        self.assertEqual(len(copied), 1)

        self.assertEqual(
            copied[0].source_region_id,
            original_region.id
        )
    
    def test_reject_snapshot_with_different_world(self):
        # Cria um segundo World.
        other_world = self.worlds.add(
            World(name="Mundo B")
        )

        assert other_world.id is not None

        # Cria uma Region exclusiva do segundo World.
        other_region = self.regions.add(
            Region(
                world_id=other_world.id,
                name="Região do Mundo B"
            )
        )

        assert other_region.id is not None

        # Obtém outra instância da Campaign original.
        stale_campaign = next(
            campaign
            for campaign in self.campaigns.get_all()
            if campaign.id == self.campaign_id
        )

        # Altera somente o objeto em memória.
        # O SQLite continua associado ao Mundo A.
        stale_campaign.world_id = other_world.id

        self.assertNotEqual(
            stale_campaign.world_id,
            self.campaign.world_id
        )

        # O snapshot deve rejeitar essa divergência.
        with self.assertRaisesRegex(
            ValueError,
            "mundo"
        ):
            self.snapshot_service.create_initial_snapshot(
                stale_campaign
            )

        # Nenhuma Region indevida deve ser copiada.
        copied = self.campaign_regions.get_all_by_campaign(
            self.campaign_id
        )

        self.assertEqual(copied, [])

        # A Campaign deve permanecer sem snapshot.
        row = self.database.connection.execute(
            """
            SELECT world_id, snapshot_created_at
            FROM campaigns
            WHERE id = ?
            """,
            (self.campaign_id,)
        ).fetchone()

        assert row is not None

        self.assertEqual(
            row["world_id"],
            self.world_id
        )

        self.assertIsNone(
            row["snapshot_created_at"]
        )
    
if __name__ == "__main__":
    unittest.main()

