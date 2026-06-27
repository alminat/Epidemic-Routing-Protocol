import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Učitavanje podataka
df = pd.read_csv("treci_scenarij_broj_cvorova.csv")
df = df.sort_values("nWifis")

fig, ax1 = plt.subplots(figsize=(13, 6))

# Delivery Ratio - lijeva osa (plava)
color_delivery = "#1f77b4"
ax1.set_xlabel("Broj čvorova (nWifis)", fontsize=13)
ax1.set_ylabel("Vjerovatnoća isporuke - Delivery Ratio [%]", fontsize=13, color=color_delivery)
line1, = ax1.plot(df["nWifis"], df["delivery_ratio"],
                  color=color_delivery, marker="o", linewidth=2,
                  markersize=6, label="Delivery Ratio (%)")
ax1.tick_params(axis="y", labelcolor=color_delivery)
ax1.set_ylim(0, 40)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

# Packet Loss - desna osa (crvena)
ax2 = ax1.twinx()
color_loss = "#d62728"
ax2.set_ylabel("Gubitak paketa - Packet Loss [%]", fontsize=13, color=color_loss)
line2, = ax2.plot(df["nWifis"], df["packet_loss"],
                  color=color_loss, marker="s", linewidth=2,
                  markersize=6, linestyle="--", label="Packet Loss (%)")
ax2.tick_params(axis="y", labelcolor=color_loss)
ax2.set_ylim(60, 110)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))

# Oznaka maksimalne vrijednosti delivery ratio
max_idx = df["delivery_ratio"].idxmax()
max_n = df.loc[max_idx, "nWifis"]
max_dr = df.loc[max_idx, "delivery_ratio"]
ax1.annotate(f"Max: {max_dr:.1f}%\n(nWifis={max_n})",
             xy=(max_n, max_dr),
             xytext=(max_n + 5, max_dr + 4),
             fontsize=10,
             color=color_delivery,
             arrowprops=dict(arrowstyle="->", color=color_delivery))

# Oznaka pada nakon maksimuma
ax1.axvline(x=max_n, color="gray", linestyle=":", linewidth=1.5, alpha=0.7)
ax1.text(max_n + 0.5, 2, f"Optimum\n({max_n} čvorova)",
         fontsize=9, color="gray", alpha=0.9)

# Legenda i naslov
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=11)

plt.title("Scenarij 3 – Uticaj broja čvorova (nWifis)\nna vjerovatnoću isporuke i gubitak paketa",
          fontsize=14, fontweight="bold", pad=15)

plt.xticks(df["nWifis"], rotation=45, fontsize=9)
plt.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()

plt.savefig("scenarij3_broj_cvorova.png", dpi=150)
plt.show()
print("Graf sačuvan kao: scenarij3_broj_cvorova.png")