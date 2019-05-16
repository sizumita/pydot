from typing import Union, IO
import os


def get_dotenv(filename: Union[str, list, tuple]):
    return DotEnv(filename)


def from_stream(stream: IO):
    return DotEnv.from_stream(stream)


class DotEnv:
    def __init__(self, file: Union[str, list, tuple] = '.env'):
        self.file = file
        self.__values = {}

    def load_dotenv(self):

        # listではなければlistに変換
        if isinstance(self.file, str):
            file = [self.file]
        else:
            file = self.file

        # fileを一つずつ読み込み
        for filename in file:

            # fileを開く
            with open(filename) as f:
                for line in f.readlines():

                    # 読み込み
                    name, value = line.split('=')

                    # 辞書に代入
                    self.__values[name] = value

    @classmethod
    def from_stream(cls, stream: IO):
        return cls(stream.name)

    def __getitem__(self, item):
        # stringではない場合エラー
        if not isinstance(item, str):
            raise ValueError(f'cannot get value with {type(item)}')

        # 読み込んだファイルに入っていれば取得
        if item in self.__values.keys():
            return self.__values[item]

        else:
            # 入っていないければosから取得
            return os.environ[item]

    def get(self, item, default=None):
        try:
            value = self.__getitem__(item)
        except KeyError:
            return default
        return value

    def to_dict(self):
        return self.__values
