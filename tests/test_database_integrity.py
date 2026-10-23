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
    find_invalid_campaign_location_region_ids
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
    
if __name__ == "__main__":
    unittest.main()
    
