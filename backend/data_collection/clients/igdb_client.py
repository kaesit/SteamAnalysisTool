"""IGDB API v4 istemcisi (Twitch Client-ID + Bearer token ile).

Steam `app_id` değerini IGDB `external_games` kaydında `uid` olarak arar
(kategori=Steam), ardından bağlı `game` nesnesinden analiz alanlarını çıkarır.
Kimlik bilgisi yoksa istemci pasif kalır; pipeline Steam verisiyle çalışmaya devam eder.
"""

import logging
import os
import time
from typing import Any, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..config import (
    IGDB_API_BASE_URL,
    IGDB_EXTERNAL_GAME_SOURCE_STEAM,
    IGDB_RATE_LIMIT_DELAY,
    REQUEST_TIMEOUT,
    REQUEST_MAX_RETRIES,
    TWITCH_OAUTH_TOKEN_URL,
)
from ..models.game_data import IgdbGameEnrichment

logger = logging.getLogger(__name__)


class IgdbClient:
    """IGDB REST istemcisi: Apicalypse gövdeli POST ve Twitch OAuth token yönetimi.

    Ortam değişkenleri:
        TWITCH_CLIENT_ID: Twitch geliştirici uygulaması Client ID (zorunlu).
        TWITCH_CLIENT_SECRET: İstemci gizli anahtarı; varsa access token otomatik alınır.
        TWITCH_ACCESS_TOKEN: Bearer token; secret yoksa doğrudan kullanılır.

    Attributes:
        client_id: Twitch Client ID.
        client_secret: İsteğe bağlı; client credentials ile token yenilemek için.
        _access_token: Bellekte tutulan OAuth access token.
    """

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
    ) -> None:
        """IgdbClient örneği oluşturur; ortam değişkenlerinden eksik alanları tamamlar."""
        self.client_id = (client_id or os.getenv("TWITCH_CLIENT_ID") or "").strip()
        self.client_secret = (
            client_secret or os.getenv("TWITCH_CLIENT_SECRET") or ""
        ).strip() or None
        self._access_token = (access_token or os.getenv("TWITCH_ACCESS_TOKEN") or "").strip() or None
        self._session = self._create_session_with_retries()
        logger.info(
            "IgdbClient initialized (configured=%s)",
            self.is_configured(),
        )

    def is_configured(self) -> bool:
        """IGDB çağrısı yapılabilir mi (Client ID + geçerli token yolu mevcut mu)?."""
        if not self.client_id:
            return False
        return bool(self._access_token or self.client_secret)

    def _create_session_with_retries(self) -> requests.Session:
        """POST istekleri için retry stratejili oturum oluşturur."""
        session = requests.Session()
        retry_strategy = Retry(
            total=REQUEST_MAX_RETRIES,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session

    def _fetch_app_access_token(self) -> Optional[str]:
        """Twitch OAuth2 client_credentials ile access token alır (secret gerekir)."""
        if not self.client_id or not self.client_secret:
            return None
        try:
            response = self._session.post(
                TWITCH_OAUTH_TOKEN_URL,
                params={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "client_credentials",
                },
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            token = data.get("access_token")
            if not token:
                logger.error("Twitch token yanıtında access_token yok")
                return None
            logger.info("Twitch app access token başarıyla alındı")
            return str(token)
        except requests.RequestException as exc:
            logger.error("Twitch OAuth token alınamadı: %s", exc)
            return None

    def _ensure_access_token(self) -> bool:
        """Bearer token yoksa secret ile yeniler; başarılıysa True döner."""
        if self._access_token:
            return True
        token = self._fetch_app_access_token()
        if token:
            self._access_token = token
            return True
        return False

    def _headers(self) -> Optional[dict[str, str]]:
        """IGDB için Client-ID ve Authorization başlıklarını üretir."""
        if not self._ensure_access_token() or not self._access_token:
            return None
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
        }

    def _post_apicalypse(self, path: str, body: str) -> Optional[list]:
        """IGDB v4 uç noktasına Apicalypse gövdesi ile POST atar."""
        headers = self._headers()
        if not headers:
            return None
        url = f"{IGDB_API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"
        time.sleep(IGDB_RATE_LIMIT_DELAY)
        try:
            response = self._session.post(
                url,
                headers=headers,
                data=body.encode("utf-8"),
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code == 401 and self.client_secret:
                logger.warning("IGDB 401; access token yenileniyor")
                self._access_token = None
                headers = self._headers()
                if not headers:
                    return None
                response = self._session.post(
                    url,
                    headers=headers,
                    data=body.encode("utf-8"),
                    timeout=REQUEST_TIMEOUT,
                )
            response.raise_for_status()
            data = response.json()
            return data if isinstance(data, list) else None
        except requests.RequestException as exc:
            logger.error("IGDB isteği başarısız (%s): %s", path, exc)
            return None
        except ValueError as exc:
            logger.error("IGDB JSON parse hatası: %s", exc)
            return None

    @staticmethod
    def _join_names(items: Optional[List[Any]], key: str = "name") -> str:
        """IGDB iç içe listelerinden `name` (veya key) alanlarını virgülle birleştirir."""
        if not items:
            return ""
        names: List[str] = []
        for item in items:
            if not isinstance(item, dict):
                continue
            val = item.get(key)
            if val:
                names.append(str(val))
        return ", ".join(names)

    @staticmethod
    def _involved_company_names(
        involved: Optional[List[Any]], *, publisher: bool, developer: bool
    ) -> str:
        """involved_companies listesinden yayıncı veya geliştirici rolüne göre isim toplar."""
        if not involved:
            return ""
        names: List[str] = []
        for row in involved:
            if not isinstance(row, dict):
                continue
            if publisher and not row.get("publisher"):
                continue
            if developer and not row.get("developer"):
                continue
            company = row.get("company") or {}
            if isinstance(company, dict):
                n = company.get("name")
                if n:
                    names.append(str(n))
        return ", ".join(names)

    @staticmethod
    def _parse_game_node(game: dict) -> IgdbGameEnrichment:
        """IGDB `game` JSON nesnesini düz IgdbGameEnrichment modeline dönüştürür."""
        genres = IgdbClient._join_names(game.get("genres"))
        themes = IgdbClient._join_names(game.get("themes"))
        modes = IgdbClient._join_names(game.get("game_modes"))
        platforms = IgdbClient._join_names(game.get("platforms"))
        involved = game.get("involved_companies")
        developers = IgdbClient._involved_company_names(
            involved if isinstance(involved, list) else None,
            publisher=False,
            developer=True,
        )
        publishers = IgdbClient._involved_company_names(
            involved if isinstance(involved, list) else None,
            publisher=True,
            developer=False,
        )

        def _f(val: Any) -> Optional[float]:
            if val is None:
                return None
            try:
                return float(val)
            except (TypeError, ValueError):
                return None

        def _i(val: Any) -> Optional[int]:
            if val is None:
                return None
            try:
                return int(val)
            except (TypeError, ValueError):
                return None

        return IgdbGameEnrichment(
            igdb_id=_i(game.get("id")),
            summary=str(game.get("summary") or ""),
            storyline=str(game.get("storyline") or ""),
            rating=_f(game.get("rating")),
            aggregated_rating=_f(game.get("aggregated_rating")),
            total_rating=_f(game.get("total_rating")),
            first_release_date_unix=_i(game.get("first_release_date")),
            genres=genres,
            themes=themes,
            game_modes=modes,
            platforms=platforms,
            developers=developers,
            publishers=publishers,
        )

    def fetch_enrichment_for_steam_app_id(
        self, steam_app_id: int
    ) -> Optional[IgdbGameEnrichment]:
        """Verilen Steam mağaza `app_id` için IGDB oyun zenginleştirmesini getirir.

        `external_games` üzerinden Steam `external_game_source` ve `uid` eşleşmesi kullanılır.
        Kimlik bilgisi yoksa veya eşleşme yoksa None döner (sessiz düşüş).

        Args:
            steam_app_id: Steam uygulama kimliği (sayı).

        Returns:
            IgdbGameEnrichment veya None.
        """
        if not self.is_configured():
            logger.debug("IGDB yapılandırılmadı; zenginleştirme atlanıyor")
            return None

        uid = str(int(steam_app_id))
        body = (
            "fields game.id, game.name, game.summary, game.storyline, "
            "game.rating, game.aggregated_rating, game.total_rating, "
            "game.first_release_date, game.genres.name, game.themes.name, "
            "game.game_modes.name, game.platforms.name, "
            "game.involved_companies.developer, game.involved_companies.publisher, "
            "game.involved_companies.company.name; "
            f"where external_game_source = {IGDB_EXTERNAL_GAME_SOURCE_STEAM} "
            f'& uid = "{uid}"; '
            "limit 1;"
        )
        rows = self._post_apicalypse("external_games", body)
        if not rows:
            logger.info("IGDB eşlemesi bulunamadı (Steam app_id=%s)", steam_app_id)
            return None
        first = rows[0] if isinstance(rows[0], dict) else None
        if not first:
            return None
        game = first.get("game")
        if not isinstance(game, dict):
            logger.warning("IGDB yanıtında game nesnesi yok (app_id=%s)", steam_app_id)
            return None
        enrichment = self._parse_game_node(game)
        logger.info(
            "IGDB zenginleştirme alındı: igdb_id=%s steam_app_id=%s",
            enrichment.igdb_id,
            steam_app_id,
        )
        return enrichment
