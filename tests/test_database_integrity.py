import sqlite3
import unittest

from src.core.database import Database

from src.core.database_audit import (
    find_orphan_region_ids,
    find_orphan_location_region_ids,
    find_orphan_location_parent_ids,
    find_location_parent_region_mismatch_ids,
    find_orphan_campaign_region_ids,
    find_orphan_campaign_location_ids,
    find_invalid_campaign_location_region_ids,
    find_orphan_campaign_location_parent_ids,
    find_campaign_location_parent_mismatch_ids,
    find_orphan_campaign_faction_ids,
    find_orphan_campaign_world_ids,
    find_orphan_faction_world_ids,
    audit_database_integrity
)


class DatabaseIntegrityTests(unittest.TestCase):

    def setUp(self):
        self.database = Database(":memory:")
        self.addCleanup(self.database.close)

    def test_foreign_keys_enabled_on_connection(self):
        connection = self.database.connection

        # A conexão deve ativar foreign_keys
        # automaticamente.
        result = connection.execute(
            "PRAGMA foreign_keys"
        ).fetchone()

        assert result is not None

        self.assertEqual(
            result[0],
            1
        )

        # Cria tabelas temporárias de teste.
        connection.execute(
            """
            CREATE TABLE test_parent (
                id INTEGER PRIMARY KEY
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE test_child (
                id INTEGER PRIMARY KEY,
                parent_id INTEGER NOT NULL,
                FOREIGN KEY (parent_id)
                    REFERENCES test_parent(id)
            )
            """
        )

        # Uma referência inexistente deve ser
        # rejeitada diretamente pelo SQLite.
        with self.assertRaises(
            sqlite3.IntegrityError
        ):
            connection.execute(
                """
                INSERT INTO test_child (
                    parent_id
                )
                VALUES (999999)
                """
            )

    def test_detect_orphan_regions_without_modifying_data(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria um World válido.
        cursor = connection.execute(
            """
            INSERT INTO worlds (name)
            VALUES (?)
            """,
            ("Mundo válido",)
        )

        world_id = cursor.lastrowid

        # Region corretamente vinculada.
        connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (world_id, "Região válida")
        )

        # Region vinculada a um World inexistente.
        cursor = connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (999_999, "Região órfã")
        )

        orphan_id = cursor.lastrowid

        before = connection.execute(
            "SELECT COUNT(*) FROM regions"
        ).fetchone()[0]

        # Executa a auditoria.
        orphan_ids = find_orphan_region_ids(
            connection
        )

        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # Nenhum registro deve ser modificado.
        after = connection.execute(
            "SELECT COUNT(*) FROM regions"
        ).fetchone()[0]

        self.assertEqual(before, after)

        # A Region órfã continua preservada.
        saved = connection.execute(
            """
            SELECT id
            FROM regions
            WHERE id = ?
            """,
            (orphan_id,)
        ).fetchone()

        self.assertIsNotNone(saved)
    
    def test_detect_locations_with_nonexistent_regions(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria um World válido.
        cursor = connection.execute(
            """
            INSERT INTO worlds (name)
            VALUES (?)
            """,
            ("Mundo válido",)
        )

        world_id = cursor.lastrowid

        # Cria uma Region válida.
        cursor = connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (world_id, "Região válida")
        )

        region_id = cursor.lastrowid

        # Cria uma Location válida.
        connection.execute(
            """
            INSERT INTO locations (region_id, name)
            VALUES (?, ?)
            """,
            (region_id, "Cidade válida")
        )

        # Cria uma Location com Region inexistente.
        cursor = connection.execute(
            """
            INSERT INTO locations (region_id, name)
            VALUES (?, ?)
            """,
            (999_999, "Cidade órfã")
        )

        orphan_id = cursor.lastrowid

        before = connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0]

        # Executa a auditoria.
        orphan_ids = find_orphan_location_region_ids(
            connection
        )

        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # Verifica que nenhum registro foi alterado.
        after = connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0]

        self.assertEqual(before, after)

        # A Location órfã continua preservada.
        saved = connection.execute(
            """
            SELECT region_id, name
            FROM locations
            WHERE id = ?
            """,
            (orphan_id,)
        ).fetchone()

        self.assertIsNotNone(saved)
        self.assertEqual(saved["region_id"], 999_999)
        self.assertEqual(saved["name"], "Cidade órfã")
    
    def test_detect_locations_with_nonexistent_parents(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria World e Region válidos.
        world = connection.execute(
            "INSERT INTO worlds (name) VALUES (?)",
            ("Mundo válido",)
        )

        region = connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (world.lastrowid, "Região válida")
        )

        region_id = region.lastrowid

        # Location raiz: parent_location_id = NULL.
        parent = connection.execute(
            """
            INSERT INTO locations (region_id, name)
            VALUES (?, ?)
            """,
            (region_id, "Cidade")
        )

        # Sublocal com pai existente.
        connection.execute(
            """
            INSERT INTO locations (
                region_id,
                parent_location_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                region_id,
                parent.lastrowid,
                "Castelo válido"
            )
        )

        # Sublocal cujo pai não existe.
        orphan = connection.execute(
            """
            INSERT INTO locations (
                region_id,
                parent_location_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                region_id,
                999_999,
                "Castelo órfão"
            )
        )

        orphan_id = orphan.lastrowid

        before = connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0]

        orphan_ids = find_orphan_location_parent_ids(
            connection
        )

        # Somente o sublocal com pai inexistente
        # deve ser identificado.
        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # A auditoria não deve modificar registros.
        after = connection.execute(
            "SELECT COUNT(*) FROM locations"
        ).fetchone()[0]

        self.assertEqual(before, after)

        saved = connection.execute(
            """
            SELECT parent_location_id
            FROM locations
            WHERE id = ?
            """,
            (orphan_id,)
        ).fetchone()

        self.assertIsNotNone(saved)
        self.assertEqual(
            saved["parent_location_id"],
            999_999
        )
    
    def test_detect_locations_with_parent_from_another_region(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria um World válido.
        world = connection.execute(
            """
            INSERT INTO worlds (name)
            VALUES (?)
            """,
            ("Mundo de teste",)
        )

        world_id = world.lastrowid

        # Cria duas Regions no mesmo World.
        region_a = connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (world_id, "Região A")
        )

        region_b = connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (world_id, "Região B")
        )

        # Cria uma Location raiz na Region A.
        parent = connection.execute(
            """
            INSERT INTO locations (region_id, name)
            VALUES (?, ?)
            """,
            (region_a.lastrowid, "Cidade A")
        )

        parent_id = parent.lastrowid

        # Sublocal válido: mesma Region do pai.
        connection.execute(
            """
            INSERT INTO locations (
                region_id,
                parent_location_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                region_a.lastrowid,
                parent_id,
                "Castelo válido"
            )
        )

        # Sublocal inválido: pertence à Region B,
        # mas seu pai pertence à Region A.
        invalid = connection.execute(
            """
            INSERT INTO locations (
                region_id,
                parent_location_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                region_b.lastrowid,
                parent_id,
                "Castelo inválido"
            )
        )

        invalid_id = invalid.lastrowid

        before = connection.execute(
            """
            SELECT id, region_id, parent_location_id
            FROM locations
            ORDER BY id
            """
        ).fetchall()

        before = [tuple(row) for row in before]

        # Executa a auditoria.
        mismatched_ids = (
            find_location_parent_region_mismatch_ids(
                connection
            )
        )

        self.assertEqual(
            mismatched_ids,
            [invalid_id]
        )

        # Confirma que a auditoria não modificou
        # nenhum relacionamento.
        after = connection.execute(
            """
            SELECT id, region_id, parent_location_id
            FROM locations
            ORDER BY id
            """
        ).fetchall()

        after = [tuple(row) for row in after]

        self.assertEqual(before, after)
    
    def test_detect_campaign_regions_without_campaign(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria uma Campaign válida.
        campaign = connection.execute(
            """
            INSERT INTO campaigns (name)
            VALUES (?)
            """,
            ("Campanha válida",)
        )

        campaign_id = campaign.lastrowid

        # CampaignRegion válida.
        # source_region_id é uma referência histórica:
        # não precisa existir no World atualmente.
        valid = connection.execute(
            """
            INSERT INTO campaign_regions (
                campaign_id,
                source_region_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                campaign_id,
                888_888,
                "Região histórica"
            )
        )

        valid_id = valid.lastrowid

        # CampaignRegion órfã: Campaign inexistente.
        orphan = connection.execute(
            """
            INSERT INTO campaign_regions (
                campaign_id,
                name
            )
            VALUES (?, ?)
            """,
            (
                999_999,
                "Região órfã"
            )
        )

        orphan_id = orphan.lastrowid

        before = [
            tuple(row)
            for row in connection.execute(
                """
                SELECT id, campaign_id, source_region_id
                FROM campaign_regions
                ORDER BY id
                """
            ).fetchall()
        ]

        orphan_ids = find_orphan_campaign_region_ids(
            connection
        )

        # Somente o registro com Campaign inexistente.
        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # A referência histórica é permitida.
        self.assertNotIn(
            valid_id,
            orphan_ids
        )

        # A auditoria não modifica os registros.
        after = [
            tuple(row)
            for row in connection.execute(
                """
                SELECT id, campaign_id, source_region_id
                FROM campaign_regions
                ORDER BY id
                """
            ).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_campaign_locations_without_campaign(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria uma Campaign válida.
        campaign = connection.execute(
            """
            INSERT INTO campaigns (name)
            VALUES (?)
            """,
            ("Campanha válida",)
        )

        campaign_id = campaign.lastrowid

        # Cria uma CampaignRegion válida.
        region = connection.execute(
            """
            INSERT INTO campaign_regions (
                campaign_id,
                name
            )
            VALUES (?, ?)
            """,
            (campaign_id, "Região válida")
        )

        region_id = region.lastrowid

        # CampaignLocation válida.
        # O source_location_id é uma referência
        # histórica e não precisa existir no World.
        valid = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id,
                region_id,
                source_location_id,
                name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_id,
                region_id,
                888_888,
                "Cidade histórica"
            )
        )

        valid_id = valid.lastrowid

        # CampaignLocation com Campaign inexistente.
        orphan = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id,
                region_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                999_999,
                region_id,
                "Cidade órfã"
            )
        )

        orphan_id = orphan.lastrowid

        # Captura o estado anterior à auditoria.
        before = [
            tuple(row)
            for row in connection.execute(
                """
                SELECT
                    id,
                    campaign_id,
                    region_id,
                    source_location_id
                FROM campaign_locations
                ORDER BY id
                """
            ).fetchall()
        ]

        orphan_ids = find_orphan_campaign_location_ids(
            connection
        )

        # Apenas a Location com Campaign inexistente
        # deve ser identificada.
        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # A referência histórica é permitida.
        self.assertNotIn(
            valid_id,
            orphan_ids
        )

        # A auditoria não pode modificar dados.
        after = [
            tuple(row)
            for row in connection.execute(
                """
                SELECT
                    id,
                    campaign_id,
                    region_id,
                    source_location_id
                FROM campaign_locations
                ORDER BY id
                """
            ).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_campaign_locations_with_invalid_regions(self):
        self.database.create_tables()
        connection = self.database.connection

        # Cria duas Campaigns independentes.
        campaign_a_id = connection.execute(
            "INSERT INTO campaigns (name) VALUES (?)",
            ("Campanha A",)
        ).lastrowid

        campaign_b_id = connection.execute(
            "INSERT INTO campaigns (name) VALUES (?)",
            ("Campanha B",)
        ).lastrowid

        # Cada Campaign possui sua própria Region.
        region_a_id = connection.execute(
            """
            INSERT INTO campaign_regions (campaign_id, name)
            VALUES (?, ?)
            """,
            (campaign_a_id, "Região A")
        ).lastrowid

        region_b_id = connection.execute(
            """
            INSERT INTO campaign_regions (campaign_id, name)
            VALUES (?, ?)
            """,
            (campaign_b_id, "Região B")
        ).lastrowid

        # Location válida, com referência histórica.
        valid_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id,
                source_location_id, name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_a_id,
                region_a_id,
                888_888,
                "Cidade válida"
            )
        ).lastrowid

        # Caso 1: Region inexistente.
        missing_region_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id, name
            )
            VALUES (?, ?, ?)
            """,
            (
                campaign_a_id,
                999_999,
                "Cidade sem região"
            )
        ).lastrowid

        # Caso 2: Region existente, mas de outra Campaign.
        wrong_campaign_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id, name
            )
            VALUES (?, ?, ?)
            """,
            (
                campaign_a_id,
                region_b_id,
                "Cidade de outra campanha"
            )
        ).lastrowid

        # Registra o estado anterior.
        query = """
            SELECT id, campaign_id, region_id,
                source_location_id
            FROM campaign_locations
            ORDER BY id
        """

        before = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        # Executa a auditoria.
        invalid_ids = (
            find_invalid_campaign_location_region_ids(
                connection
            )
        )

        self.assertEqual(
            invalid_ids,
            [missing_region_id, wrong_campaign_id]
        )

        # A Location válida não deve ser identificada.
        self.assertNotIn(valid_id, invalid_ids)

        # Nenhum relacionamento deve ser modificado.
        after = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_campaign_locations_with_nonexistent_parents(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria uma Campaign válida.
        campaign_id = connection.execute(
            """
            INSERT INTO campaigns (name)
            VALUES (?)
            """,
            ("Campanha de teste",)
        ).lastrowid

        # Cria uma CampaignRegion válida.
        region_id = connection.execute(
            """
            INSERT INTO campaign_regions (
                campaign_id,
                name
            )
            VALUES (?, ?)
            """,
            (campaign_id, "Região de teste")
        ).lastrowid

        # Location raiz: não possui pai.
        parent_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id,
                region_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                campaign_id,
                region_id,
                "Cidade"
            )
        ).lastrowid

        # Sublocal válido: pai existente.
        valid_child_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id,
                region_id,
                parent_location_id,
                name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_id,
                region_id,
                parent_id,
                "Castelo válido"
            )
        ).lastrowid

        # Sublocal inválido: pai inexistente.
        orphan_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id,
                region_id,
                parent_location_id,
                name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_id,
                region_id,
                999_999,
                "Torre órfã"
            )
        ).lastrowid

        query = """
            SELECT
                id,
                campaign_id,
                region_id,
                parent_location_id
            FROM campaign_locations
            ORDER BY id
        """

        before = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        # Executa a auditoria.
        orphan_ids = (
            find_orphan_campaign_location_parent_ids(
                connection
            )
        )

        # Apenas o sublocal com pai inexistente.
        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # A Location raiz e o filho válido
        # não devem ser identificados.
        self.assertNotIn(parent_id, orphan_ids)
        self.assertNotIn(valid_child_id, orphan_ids)

        # Confirma que nenhum dado foi alterado.
        after = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_campaign_locations_with_invalid_parent_ownership(self):
        self.database.create_tables()
        connection = self.database.connection

        # Cria duas Campaigns independentes.
        campaign_a_id = connection.execute(
            "INSERT INTO campaigns (name) VALUES (?)",
            ("Campanha A",)
        ).lastrowid

        campaign_b_id = connection.execute(
            "INSERT INTO campaigns (name) VALUES (?)",
            ("Campanha B",)
        ).lastrowid

        # Duas Regions na Campaign A.
        region_a1_id = connection.execute(
            """
            INSERT INTO campaign_regions (campaign_id, name)
            VALUES (?, ?)
            """,
            (campaign_a_id, "Região A1")
        ).lastrowid

        region_a2_id = connection.execute(
            """
            INSERT INTO campaign_regions (campaign_id, name)
            VALUES (?, ?)
            """,
            (campaign_a_id, "Região A2")
        ).lastrowid

        # Uma Region na Campaign B.
        region_b_id = connection.execute(
            """
            INSERT INTO campaign_regions (campaign_id, name)
            VALUES (?, ?)
            """,
            (campaign_b_id, "Região B")
        ).lastrowid

        # Location pai válida na Campaign A.
        parent_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id, name
            )
            VALUES (?, ?, ?)
            """,
            (campaign_a_id, region_a1_id, "Cidade A")
        ).lastrowid

        # Filho válido: mesma Campaign e Region.
        valid_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id,
                parent_location_id, name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_a_id,
                region_a1_id,
                parent_id,
                "Castelo válido"
            )
        ).lastrowid

        # Caso 1: mesma Campaign, Region diferente.
        wrong_region_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id,
                parent_location_id, name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_a_id,
                region_a2_id,
                parent_id,
                "Castelo de outra região"
            )
        ).lastrowid

        # Caso 2: Campaign diferente.
        wrong_campaign_id = connection.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id, region_id,
                parent_location_id, name
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                campaign_b_id,
                region_b_id,
                parent_id,
                "Castelo de outra campanha"
            )
        ).lastrowid

        query = """
            SELECT
                id,
                campaign_id,
                region_id,
                parent_location_id
            FROM campaign_locations
            ORDER BY id
        """

        before = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        # Executa a auditoria.
        invalid_ids = (
            find_campaign_location_parent_mismatch_ids(
                connection
            )
        )

        self.assertEqual(
            invalid_ids,
            [wrong_region_id, wrong_campaign_id]
        )

        # Registros válidos não devem aparecer.
        self.assertNotIn(parent_id, invalid_ids)
        self.assertNotIn(valid_id, invalid_ids)

        # Nenhum relacionamento pode ser alterado.
        after = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_campaign_factions_without_campaign(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria uma Campaign válida.
        campaign_id = connection.execute(
            """
            INSERT INTO campaigns (name)
            VALUES (?)
            """,
            ("Campanha válida",)
        ).lastrowid

        # Faction válida com referência histórica.
        # Não é necessário que a Faction original exista.
        valid_id = connection.execute(
            """
            INSERT INTO campaign_factions (
                campaign_id,
                source_faction_id,
                name
            )
            VALUES (?, ?, ?)
            """,
            (
                campaign_id,
                888_888,
                "Ordem dos Magos"
            )
        ).lastrowid

        # Faction inválida: Campaign inexistente.
        orphan_id = connection.execute(
            """
            INSERT INTO campaign_factions (
                campaign_id,
                name
            )
            VALUES (?, ?)
            """,
            (
                999_999,
                "Facção órfã"
            )
        ).lastrowid

        query = """
            SELECT
                id,
                campaign_id,
                source_faction_id,
                name
            FROM campaign_factions
            ORDER BY id
        """

        before = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        # Executa a auditoria.
        orphan_ids = find_orphan_campaign_faction_ids(
            connection
        )

        # Apenas a Faction sem Campaign deve aparecer.
        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # A referência histórica não é um erro.
        self.assertNotIn(
            valid_id,
            orphan_ids
        )

        # Nenhum registro pode ser modificado.
        after = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_campaigns_with_nonexistent_worlds(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria um World válido.
        world_id = connection.execute(
            """
            INSERT INTO worlds (name)
            VALUES (?)
            """,
            ("Mundo válido",)
        ).lastrowid

        # Campaign associada a um World existente.
        valid_id = connection.execute(
            """
            INSERT INTO campaigns (name, world_id)
            VALUES (?, ?)
            """,
            ("Campanha válida", world_id)
        ).lastrowid

        # Campaign sem World: situação permitida.
        no_world_id = connection.execute(
            """
            INSERT INTO campaigns (name, world_id)
            VALUES (?, NULL)
            """,
            ("Campanha sem mundo",)
        ).lastrowid

        # Campaign com World inexistente.
        orphan_id = connection.execute(
            """
            INSERT INTO campaigns (name, world_id)
            VALUES (?, ?)
            """,
            ("Campanha órfã", 999_999)
        ).lastrowid

        query = """
            SELECT
                id,
                name,
                world_id,
                snapshot_created_at
            FROM campaigns
            ORDER BY id
        """

        before = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        # Executa a auditoria.
        orphan_ids = find_orphan_campaign_world_ids(
            connection
        )

        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # Campaigns válidas não devem aparecer.
        self.assertNotIn(valid_id, orphan_ids)
        self.assertNotIn(no_world_id, orphan_ids)

        # A auditoria não pode modificar registros.
        after = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_detect_factions_with_nonexistent_worlds(self):
        self.database.create_tables()

        connection = self.database.connection

        # Cria um World válido.
        world_id = connection.execute(
            """
            INSERT INTO worlds (name)
            VALUES (?)
            """,
            ("Mundo válido",)
        ).lastrowid

        # Faction corretamente associada ao World.
        valid_id = connection.execute(
            """
            INSERT INTO factions (world_id, name)
            VALUES (?, ?)
            """,
            (
                world_id,
                "Ordem dos Magos"
            )
        ).lastrowid

        # Faction com World inexistente.
        orphan_id = connection.execute(
            """
            INSERT INTO factions (world_id, name)
            VALUES (?, ?)
            """,
            (
                999_999,
                "Facção órfã"
            )
        ).lastrowid

        query = """
            SELECT id, world_id, name
            FROM factions
            ORDER BY id
        """

        before = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        # Executa a auditoria.
        orphan_ids = find_orphan_faction_world_ids(
            connection
        )

        # Apenas a Faction sem World deve aparecer.
        self.assertEqual(
            orphan_ids,
            [orphan_id]
        )

        # A Faction válida não deve aparecer.
        self.assertNotIn(
            valid_id,
            orphan_ids
        )

        # A auditoria não pode modificar registros.
        after = [
            tuple(row)
            for row in connection.execute(query).fetchall()
        ]

        self.assertEqual(before, after)
    
    def test_consolidated_database_integrity_audit(self):
        self.database.create_tables()
        connection = self.database.connection

        # Banco inicialmente sem inconsistências.
        empty_report = audit_database_integrity(
            connection
        )

        self.assertEqual(len(empty_report), 12)

        self.assertTrue(
            all(
                len(ids) == 0
                for ids in empty_report.values()
            )
        )

        # Cria duas inconsistências independentes.
        orphan_region_id = connection.execute(
            """
            INSERT INTO regions (world_id, name)
            VALUES (?, ?)
            """,
            (999_999, "Região órfã")
        ).lastrowid

        orphan_faction_id = connection.execute(
            """
            INSERT INTO factions (world_id, name)
            VALUES (?, ?)
            """,
            (999_999, "Facção órfã")
        ).lastrowid

        # Registra a quantidade de alterações.
        changes_before = connection.total_changes

        # Executa todas as auditorias.
        report = audit_database_integrity(
            connection
        )

        self.assertEqual(
            report["regions_without_world"],
            [orphan_region_id]
        )

        self.assertEqual(
            report["factions_without_world"],
            [orphan_faction_id]
        )

        # As demais verificações devem estar vazias.
        for name, ids in report.items():
            if name not in (
                "regions_without_world",
                "factions_without_world"
            ):
                self.assertEqual(ids, [])

        # O diagnóstico não pode alterar registros.
        self.assertEqual(
            connection.total_changes,
            changes_before
        )
    
    def test_read_schema_version_without_modifying_it(self):
        self.database.create_tables()

        connection = self.database.connection

        # Bancos novos ainda não possuem
        # migrations versionadas.
        self.assertEqual(
            self.database.get_schema_version(),
            0
        )

        # Simula uma versão diferente apenas no
        # banco temporário em memória deste teste.
        connection.execute(
            "PRAGMA user_version = 3"
        )

        # O método deve ler a versão real.
        self.assertEqual(
            self.database.get_schema_version(),
            3
        )

        # A consulta não deve modificar a versão.
        row = connection.execute(
            "PRAGMA user_version"
        ).fetchone()

        self.assertIsNotNone(row)

        self.assertEqual(
            row[0],
            3
        )
    
if __name__ == "__main__":
    unittest.main()
    
