import json
import itertools

SPDX_LICENSES_GRAMS = '/home/moonsun/spdx_project/spdx_license_data_grams.json'

class TokenComapre: 
    def __init__(self):
        pass
    
    def lcs_lens(self, xs, ys):
        length = list(itertools.repeat(0, 1 + len(ys)))
        for x in xs:
            prev = list(length)
            for i, y in enumerate(ys):
                if x == y:
                    length[i + 1] = prev[i] + 1
                else:
                    length[i + 1] = max(length[i], prev[i + 1])
        return length


    def lcs(self, xs, ys):
        nx, ny = len(xs), len(ys)
        if nx == 0:
            return []
        elif nx == 1:
            return [xs[0]] if xs[0] in ys else []
        else:
            i = nx // 2
            xb, xe = xs[:i], xs[i:]
            ll_b = self.lcs_lens(xb, ys)
            ll_e = self.lcs_lens(xe[::-1], ys[::-1])
            _, k = max((ll_b[j] + ll_e[ny - j], j)
                        for j in range(ny + 1))
            yb, ye = ys[:k], ys[k:]

            return self.lcs(xb, yb) + self.lcs(xe, ye)


    def lcs_similarity(self, xs, ys):
        ys = tuple(ys)
        output = self.lcs(xs, ys)

        try:
            simularity = len(output) / max(len(xs), len(ys))
        except:
            simularity = 0

        return simularity