import hashlib


class _qizemjhu:
    _udzccylx = 1103515245
    _arirwwia = 12345
    _shekpakl = 1 << 31

    def __init__(_tvdrwslp, _pepchozd: int):
        _tvdrwslp._rsxxfgsi = _pepchozd & 4294967295

    def _pjtuzwnw(_tvdrwslp) -> int:
        _tvdrwslp._rsxxfgsi = (
            _tvdrwslp._udzccylx * _tvdrwslp._rsxxfgsi + _tvdrwslp._arirwwia
        ) % _tvdrwslp._shekpakl
        return _tvdrwslp._rsxxfgsi >> 16 & 32767

    def _iacvxnvg(_tvdrwslp, _ieuqgvnp: int) -> bytes:
        return bytes((_tvdrwslp._pjtuzwnw() & 255 for _smtbmxwr in range(_ieuqgvnp)))


def _ilnwqzos(_wydzfmje: int) -> str:
    _rboolnui = _qizemjhu(_wydzfmje)
    _wewlqdpo = _rboolnui._iacvxnvg(16)
    _mpidngdx = hashlib.md5(_wewlqdpo).hexdigest()
    return _mpidngdx[:16]


print(f"flag=sgctf{{{_ilnwqzos(int.from_bytes(b"1n5an31y_H4rd_70_R34D_S3CR37"))}}}")
