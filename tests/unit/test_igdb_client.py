"""IgdbClient birim testleri (HTTP mock ile)."""

from unittest.mock import patch

import pytest

from data_collection.clients.igdb_client import IgdbClient
from data_collection.models.game_data import IgdbGameEnrichment


class TestIgdbClientConfigured:
    """Kimlik bilgisi varken token ve IGDB çağrı davranışı."""

    def test_is_configured_with_static_token(self):
        """Sadece Client ID + access token ile istemci yapılandırılmış sayılır."""
        client = IgdbClient(
            client_id="cid",
            client_secret=None,
            access_token="tok",
        )
        assert client.is_configured() is True

    def test_is_configured_with_secret_only(self):
        """Client ID + secret ile token çekilebilir; yapılandırılmış sayılır."""
        client = IgdbClient(
            client_id="cid",
            client_secret="sec",
            access_token=None,
        )
        assert client.is_configured() is True

    def test_not_configured_without_id(self):
        """Client ID yoksa yapılandırılmamış kabul edilir."""
        client = IgdbClient(client_id="", access_token="x")
        assert client.is_configured() is False

    @patch.object(IgdbClient, "_post_apicalypse")
    def test_fetch_enrichment_parses_game(self, mock_post):
        """external_games yanıtı IgdbGameEnrichment modele dönüşür."""
        mock_post.return_value = [
            {
                "game": {
                    "id": 99,
                    "summary": "Özet",
                    "storyline": "Hikaye",
                    "rating": 80.0,
                    "aggregated_rating": 81.0,
                    "total_rating": 79.5,
                    "first_release_date": 1234567890,
                    "genres": [{"name": "Shooter"}],
                    "themes": [{"name": "Action"}],
                    "game_modes": [{"name": "Multiplayer"}],
                    "platforms": [{"name": "PC"}],
                    "involved_companies": [
                        {
                            "developer": True,
                            "publisher": False,
                            "company": {"name": "DevCo"},
                        },
                        {
                            "developer": False,
                            "publisher": True,
                            "company": {"name": "PubCo"},
                        },
                    ],
                }
            }
        ]
        client = IgdbClient(client_id="id", access_token="token")
        out = client.fetch_enrichment_for_steam_app_id(440)
        assert isinstance(out, IgdbGameEnrichment)
        assert out.igdb_id == 99
        assert out.summary == "Özet"
        assert "Shooter" in out.genres
        assert out.developers == "DevCo"
        assert out.publishers == "PubCo"


class TestIgdbClientUnconfigured:
    """Kimlik bilgisi yokken sessiz düşüş."""

    def test_fetch_returns_none_when_not_configured(self):
        """Yapılandırma yoksa IGDB çağrısı yapılmaz ve None döner."""
        client = IgdbClient(client_id="", client_secret=None, access_token=None)
        assert client.fetch_enrichment_for_steam_app_id(730) is None
