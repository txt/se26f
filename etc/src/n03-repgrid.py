"""FOCUS-style repertory grid for N3: clustered heatmap, dendrograms above
(constructs) and right (elements). Food-delivery rivals, scores illustrative.
Regenerate: python3 n03-repgrid.py; pdftoppm -r 200 -png n03-repgrid.pdf x;
magick x-1.png -trim -bordercolor white -border 20 ../img/n03-repgrid.png"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from scipy.cluster.hierarchy import linkage, dendrogram

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Charter"],
    "font.size": 9,
    "pdf.fonttype": 42,
})

INK = "#333333"
MUTE = "#777777"
RAMP = ["#FDECEA", "#F5BDB6", "#E88A7E", "#CC5246", "#8F221A"]
CMAP = ListedColormap(RAMP)
NORM = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], CMAP.N)

def focus_grid(data, constructs, title, outfile, bold_rows=("FoodPool",)):
    names = list(data.keys())
    X = np.array([data[n] for n in names], dtype=float)
    ideal = X[0]
    dists = np.abs(X - ideal).sum(axis=1).astype(int)

    zr = linkage(X, method="ward")
    zc = linkage(X.T, method="ward")

    nrow, ncol = X.shape
    hm_w, hm_h = ncol * 0.30, nrow * 0.21
    left, bottom, top_d, right_d = 2.05, 1.75, 0.45, 0.80
    fw = left + hm_w + right_d + 0.15
    fh = bottom + hm_h + top_d + 0.30

    fig = plt.figure(figsize=(fw, fh))
    ax = fig.add_axes((left / fw, bottom / fh, hm_w / fw, hm_h / fh))
    ax_t = fig.add_axes((left / fw, (bottom + hm_h) / fh, hm_w / fw, top_d / fh), sharex=ax)
    ax_r = fig.add_axes(((left + hm_w) / fw, bottom / fh, right_d / fw, hm_h / fh), sharey=ax)

    with plt.rc_context({"lines.linewidth": 0.9}):
        dc = dendrogram(zc, ax=ax_t, orientation="top",
                        link_color_func=lambda _: MUTE, no_labels=True)
        dr = dendrogram(zr, ax=ax_r, orientation="right",
                        link_color_func=lambda _: MUTE, no_labels=True)
    for a in (ax_t, ax_r):
        a.set_axis_off()

    col_order = dc["leaves"]
    row_order = dr["leaves"]
    ax.imshow(X[np.ix_(row_order, col_order)], cmap=CMAP, norm=NORM,
              aspect="auto", origin="lower",
              extent=(0, 10 * ncol, 0, 10 * nrow), interpolation="nearest")
    for i in range(1, ncol):
        ax.axvline(10 * i, color="white", lw=1.4)
    for j in range(1, nrow):
        ax.axhline(10 * j, color="white", lw=1.4)

    for j, ri in enumerate(row_order):
        for i, ci in enumerate(col_order):
            v = int(X[ri, ci])
            ax.text(10 * i + 5, 10 * j + 5, str(v), ha="center", va="center",
                    fontsize=7.8, color="white" if v >= 4 else INK)

    ax.set_xticks([10 * i + 5 for i in range(ncol)])
    ax.set_xticklabels([constructs[c] for c in col_order],
                       rotation=40, ha="right", fontsize=7.2, color=INK,
                       rotation_mode="anchor")
    ax.set_yticks([10 * j + 5 for j in range(nrow)])
    labs = ax.set_yticklabels(
        [f"{names[r]}   d={dists[r]}" for r in row_order], fontsize=8.2, color=INK)
    for lab, r in zip(labs, row_order):
        if names[r] in bold_rows or r == 0:
            lab.set_fontweight("bold")
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)

    ax_t.set_title(title, fontsize=11, fontweight="bold", color=INK, pad=4)
    fig.savefig(outfile, format="pdf")
    plt.close(fig)
    print("wrote", outfile)



FOOD_CONSTRUCTS = [
    "1=couriers paid fairly ... 5=gig rates opaque",
    "1=low restaurant fees ... 5=30% commission",
    "1=group ordering ... 5=solo only",
    "1=accessible (WCAG) ... 5=untested",
    "1=open API ... 5=walled garden",
    "1=local independents first ... 5=chains first",
    "1=privacy respecting ... 5=data hungry",
]
FOOD = {
    "IDEAL":        [1, 1, 1, 1, 1, 1, 1],
    "MegaDash":     [4, 5, 3, 2, 4, 4, 4],
    "UrbanEats":    [4, 5, 4, 2, 3, 4, 5],
    "GrubCentral":  [3, 4, 5, 3, 3, 3, 4],
    "SliceLocal":   [2, 2, 5, 4, 2, 1, 2],
    "ChowNearby":   [2, 1, 5, 4, 3, 1, 3],
    "CampusBites":  [3, 3, 2, 5, 5, 2, 2],
    "FoodPool":     [2, 2, 1, 3, 2, 2, 2],
}
focus_grid(FOOD, FOOD_CONSTRUCTS,
           "Repertory grid - food-delivery rivals (scores illustrative)",
           "n03-repgrid.pdf", bold_rows=("FoodPool",))
