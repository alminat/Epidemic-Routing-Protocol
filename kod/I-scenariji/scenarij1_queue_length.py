import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Učitavanje podataka
df = pd.read_csv("prvi_scen.csv")

# Sortiranje po parametru
df = df.sort_values("queueLength")

fig, ax1 = plt.subplots(figsize=(12, 6))

# Delivery Ratio - lijeva osa (plava)
color_delivery = "#1f77b4"
ax1.set_xlabel("Veličina bafera (Queue Length) [paketi]", fontsize=13)
ax1.set_ylabel("Vjerovatnoća isporuke - Delivery Ratio [%]", fontsize=13, color=color_delivery)
line1, = ax1.plot(df["queueLength"], df["delivery_ratio"],
                  color=color_delivery, marker="o", linewidth=2,
                  markersize=6, label="Delivery Ratio (%)")
ax1.tick_params(axis="y", labelcolor=color_delivery)
ax1.set_ylim(0, 45)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

# Packet Loss - desna osa (crvena)
ax2 = ax1.twinx()
color_loss = "#d62728"
ax2.set_ylabel("Gubitak paketa - Packet Loss [%]", fontsize=13, color=color_loss)
line2, = ax2.plot(df["queueLength"], df["packet_loss"],
                  color=color_loss, marker="s", linewidth=2,
                  markersize=6, linestyle="--", label="Packet Loss (%)")
ax2.tick_params(axis="y", labelcolor=color_loss)
ax2.set_ylim(55, 105)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))

# Oznaka maksimalne vrijednosti delivery ratio
max_idx = df["delivery_ratio"].idxmax()
max_ql = df.loc[max_idx, "queueLength"]
max_dr = df.loc[max_idx, "delivery_ratio"]
ax1.annotate(f"Max: {max_dr:.1f}%\n(queueLength={max_ql})",
             xy=(max_ql, max_dr),
             xytext=(max_ql + 80, max_dr + 4),
             fontsize=10,
             color=color_delivery,
             arrowprops=dict(arrowstyle="->", color=color_delivery))

# Legenda i naslov
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc="upper left", fontsize=11)

plt.title("Scenarij 1 – Uticaj veličine bafera (Queue Length)\nna vjerovatnoću isporuke i gubitak paketa",
          fontsize=14, fontweight="bold", pad=15)

plt.xticks(df["queueLength"], rotation=45, fontsize=9)
plt.grid(True, linestyle="--", alpha=0.4)
fig.tight_layout()

plt.savefig("scenarij1_queue_length.png", dpi=150)
plt.show()
print("Graf sačuvan kao: scenarij1_queue_length.png")