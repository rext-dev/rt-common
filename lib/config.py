# RT Lib - Config

__all__ = ("IpcsServer", "config_file_path", "get_file_path")

from typing import TypedDict

from pathlib import PurePath

from os import getenv, mkdir
from os.path import exists

from core.rextlib.common.hash import get_file_hash


class IpcsServer(TypedDict):
    "ipcsのサーバーの接続先の設定の型です。"

    host: str
    port: int


config_file_path = getenv("RT_CONFIG_FILE_PATH", "config.toml")
REPLACEMENT = "!config_types_hash!"
def get_file_path() -> PurePath:
    """設定ファイルのパスを取得します。
    環境変数`RT_CONFIG_FILE_PATH`からパスを取得しますが、もしそれが設定されていないのなら、`config.toml`が代わりに返されます。
    もし、パスに文字列`.REPLACEMENT`が含まれているのなら、それは`core/config/types_.py`のsha256のハッシュ値と置き換えられます。"""
    global config_file_path
    if REPLACEMENT in config_file_path:
        config_file_path = config_file_path.replace(
            REPLACEMENT,
            get_file_hash("core/config/types_.py")
        )
    path = PurePath(config_file_path)
    if not exists(path.parent):
        mkdir(path.parent)
    return path