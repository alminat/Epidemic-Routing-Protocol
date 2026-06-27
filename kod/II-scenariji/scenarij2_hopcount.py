import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Učitavanje podataka
df = pd.read_csv("scenarij2_hopcount.csv")
df = df.sort_values("hopCount")

fig, ax1 = plt.subplots(figsize=(14, 6))

# Delivery Ratio - lijeva osa (plava)
color_delivery = "#1f77b4"
ax1.set_xlabel("Maksimalni broj skokova (Hop Count)", fontsize=13)
ax1.set_ylabel("Vjerovatnoća isporuke - Delivery Ratio [%]", fontsize=13, color=color_delivery)
line1, = ax1.plot(df["hopCount"], df["delivery_ratio"],
                  color=color_delivery, marker="o", linewidth=2,
                  markersize=5, label="Delivery Ratio (%)")
ax1.tick_params(axis="y", labelcolor=color_delivery)
ax1.set_ylim(0, 45)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

# Packet Loss - desna osa (crvena)
ax2 = ax1.twinx()
color_loss = "#d62728"
ax2.set_ylabel("Gubitak paketa / Mrežni overhead", fontsize=13, color="black")
line2, = ax2.plot(df["hopCount"], df["packet_loss"],
                  color=color_loss, marker="s", linewidth=2,
                  markersize=5, linestyle="--", label="Packet Loss (%)")

# Overhead - desna osa (zelena)
color_overhead = "#2ca02c"
line3, = ax2.plot(df["hopCount"], df["overhead"],
                  color=color_overhead, marker="^", linewidth=2,
                  markersize=5, linestyle=":", label="Overhead")

ax2.tick_params(axis="y", labelcolor="black")
ax2.set_ylim(0, 105)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))

# Oznaka maksimalne vrijednosti delivery ratio
max_idx = df["delivery_ratio"].idxmax()
max_hc = df.loc[max_idx, "hopCount"]
max_dr = df.loc[max_idx, "delivery_ratio"]
ax1.annotate(f"Max: {max_dr:.1f}%\n(hopCount={max_hc})",
             xy=(max_hc, max_dr),
             xytext=(max_hc + 3, max_dr + 5),
             fontsize=10,
             color=color_delivery,
             arrowprops=dict(arrowstyle="->", color=color_delivery))

# Legenda i naslov
lines = [line1, line2, line3]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper right", fontsize=11)

plt.title("Scenarij 2 – Uticaj maksimalnog broja skokova (Hop Count)\nna vjerovatnoću isporuke, gubitak paketa i mrežni overhead",
          fontsize=14, fontweight="bold", pad=15)

plt.xticks(df["hopCount"], rotation=90, fontsize=8)
plt.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()

plt.savefig("scenarij2_hopcount.png", dpi=150)
plt.show()
print("Graf sačuvan kao: scenarij2_hopcount.png")