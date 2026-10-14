import unittest
from types import SimpleNamespace
from unittest.mock import Mock

import pygame

from src.screens.campaign.factions.list import (
    FactionScreen,
    FactionViewMode,
)


class CampaignFactionEventTests(unittest.TestCase):

    def setUp(self):
        # Evita inicializar fontes e a interface gráfica.
        self.screen = object.__new__(FactionScreen)

        self.screen.app = SimpleNamespace(
            current_campaign=SimpleNamespace(
                id=1,
                world_id=1,
            )
        )

        self.screen.sidebar = Mock()

        self.screen.confirm_dialog = Mock(
            visible=False
        )

        self.mock_list_event = Mock(
            return_value=(None, None)
        )

        self.mock_details_event = Mock(
            return_value=(None, None)
        )

        self.mock_form_event = Mock(
            return_value=None
        )

        self.screen.list_view = Mock(
            handle_event=self.mock_list_event
        )

        self.screen.details_view = Mock(
            handle_event=self.mock_details_event
        )

        self.screen.faction_form = Mock(
            handle_event=self.mock_form_event
        )

        self.screen.list_view.handle_event.return_value = (
            None, None
        )

        self.screen.details_view.handle_event.return_value = (
            None, None
        )

        self.screen.faction_form.handle_event.return_value = None

        self.event = SimpleNamespace(
            type=pygame.MOUSEMOTION
        )

    def test_details_event_does_not_reach_list(self):
        self.screen.view_mode = FactionViewMode.DETAILS

        self.screen.handle_event(self.event)

        self.mock_details_event.assert_called_once_with(
            self.event
        )

        self.mock_list_event.assert_not_called()

    def test_back_event_is_not_processed_by_list(self):
        self.screen.view_mode = FactionViewMode.DETAILS
        self.screen.selected_faction = object()

        self.mock_details_event.return_value = (
            "back", None
        )

        self.screen.handle_event(self.event)

        self.assertEqual(
            self.screen.view_mode,
            FactionViewMode.LIST
        )

        self.assertIsNone(self.screen.selected_faction)

        self.mock_list_event.assert_not_called()

    def test_form_event_reaches_only_form(self):
        self.screen.view_mode = FactionViewMode.FORM

        self.screen.handle_event(self.event)

        self.mock_form_event.assert_called_once_with(
            self.event
        )

        self.mock_details_event.assert_not_called()
        self.mock_list_event.assert_not_called()


if __name__ == "__main__":
    unittest.main()
