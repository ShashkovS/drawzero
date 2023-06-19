from numbers import Real
from typing import List

from drawzero.utils.errors import BadDrawParmsError
from drawzero.utils.converters import _to_color, _to_flat
from drawzero.utils.i18n import I18N
from drawzero.utils.colors import C


class Gradient:
    """Gradient — a color scale object works as a function that maps numeric values to a color palette.
    The default scale has the domain 0..1

    Example:
    >>> scale = Gradient([C.black, C.white])
    >>> scale = Gradient([C.red, C.yellow, C.green], 0, 100)
    >>> scale = Gradient([C.red, C.yellow, C.green], 0, 30, 100)
    """

    def __init__(self, colors: list, start=0.0, end=1.0, *args: List[Real]):
        error = BadDrawParmsError()
        self.colors = [_to_color(color, error) for color in colors]
        num_colors = len(self.colors)
        domain = sorted(_to_flat([start, end] + list(args)))
        if not all(isinstance(d, Real) for d in domain):
            error.errors.append(I18N.wrong_domain_types.format(domain))
        elif len(domain) == 2:
            d_len = domain[1] - domain[0]
            self.domain = [domain[0] + step / (num_colors - 1) * d_len for step in range(num_colors)]
        elif len(domain) == len(self.colors):
            self.domain = domain
        else:
            self.domain = []
            error.errors.append(I18N.wrong_domain.format(num_colors))

        if error.errors:
            if num_colors <= 2 and len(self.domain) <= 2:
                error.example = f"Gradient([C.red, C.green], 0, 100)"
            else:
                error.example = f"Gradient([C.red, C.yellow, C.green], 0, 70, 100)"
            error.finish()
            raise error

    def __call__(self, x):
        if x <= self.domain[0]:
            return self.colors[0]
        elif x >= self.domain[-1]:
            return self.colors[-1]
        d_ind = 0
        while x > self.domain[d_ind + 1]:
            d_ind += 1
        diff = self.domain[d_ind + 1] - self.domain[d_ind]
        left_color = self.colors[d_ind]
        right_color = self.colors[d_ind + 1]
        color = tuple(
            min(int(right_color[c] * (x - self.domain[d_ind]) / diff + left_color[c] * (self.domain[d_ind + 1] - x) / diff + 0.5), 255)
            for c in (0, 1, 2)
        )
        return color

    def __repr__(self):
        return f'{self.__class__.__name__}({self.colors!r}, {", ".join(map(str, self.domain))})'
