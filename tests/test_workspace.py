import unittest
from unittest.mock import patch

from src.core.app import App
from src.core.workspace import Workspace
from src.domain.campaign.models.campaign import Campaign


class WorkspaceTests(unittest.TestCase):

    def setUp(self):
        self.workspace = Workspace()

        self.campaign_a = Campaign(
            id=1,
            name="Campanha A"
        )

        self.campaign_b = Campaign(
            id=2,
            name="Campanha B"
        )

    def test_workspace_starts_without_campaign(self):
        self.assertIsNone(
            self.workspace.current_campaign
        )

    def test_select_and_replace_campaign(self):
        self.workspace.select_campaign(
            self.campaign_a
        )

        self.assertIs(
            self.workspace.current_campaign,
            self.campaign_a
        )

        self.workspace.select_campaign(
            self.campaign_b
        )

        self.assertIs(
            self.workspace.current_campaign,
            self.campaign_b
        )

    def test_close_campaign_clears_workspace(self):
        self.workspace.select_campaign(
            self.campaign_a
        )

        self.workspace.close_campaign()

        self.assertIsNone(
            self.workspace.current_campaign
        )

        # Encerrar novamente não deve causar erros.
        self.workspace.close_campaign()

        self.assertIsNone(
            self.workspace.current_campaign
        )


class AppWorkspaceCompatibilityTests(unittest.TestCase):

    def setUp(self):
        # Não inicializa Pygame nem abre o banco.
        self.app = App.__new__(App)

        self.app.workspace = Workspace()

        self.campaign = Campaign(
            id=1,
            name="Campanha de teste"
        )

    def test_app_exposes_workspace_campaign(self):
        self.assertIsNone(
            self.app.current_campaign
        )

        self.app.select_campaign(
            self.campaign
        )

        self.assertIs(
            self.app.current_campaign,
            self.campaign
        )

        self.assertIs(
            self.app.workspace.current_campaign,
            self.campaign
        )

        self.app.close_campaign()

        self.assertIsNone(
            self.app.current_campaign
        )

    def test_return_to_campaigns_clears_workspace(self):
        self.app.select_campaign(
            self.campaign
        )

        def assert_campaign_closed():
            self.assertIsNone(
                self.app.workspace.current_campaign
            )

        with patch.object(
            App,
            "open_campaigns",
            side_effect=assert_campaign_closed
        ) as open_campaigns:

            self.app.return_to_campaigns()

            open_campaigns.assert_called_once_with()

        self.assertIsNone(
            self.app.current_campaign
        )


if __name__ == "__main__":
    unittest.main()