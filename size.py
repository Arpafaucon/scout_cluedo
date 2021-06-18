from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import typing as tp

@dataclass(init=False)
class Size:
    x: float
    y: float

    def __init__(self, x, y=None):
        if y is None:
            if isinstance(x, Size):
                self.x, self.y = x.x, x.y
            else:
                assert len(x) == 2
                self.x, self.y = x
        else:
            assert isinstance(x, (float, int))
            assert isinstance(y, (float, int))
            self.x=x
            self.y=y

    @property
    def array(self) -> np.ndarray:
        return np.array([self.x, self.y])

    @array.setter
    def array(self, arr):
        assert arr.shape == (2,)
        self.x, self.y = arr

    def tuple(self) -> tp.Tuple[float, float]:
        return self.x, self.y

    def tuple_int(self) -> tp.Tuple[int, int]:
        return round(self.x), round(self.y)

    def __mul__(self, a) -> Size:
        return Size(a*self.array)