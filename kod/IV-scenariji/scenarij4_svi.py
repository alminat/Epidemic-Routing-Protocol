import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Učitavanje podataka
df = pd.read_csv("manual_results.csv")


# Podscenarij 4.1 – queueLength i hopCount (nWifis=50)
sub41 = df[(df["nWifis"] == 50)].copy()
# Uzimamo redove gdje se oba parametra mijenjaju zajedno (hopCount > 50 ili specifični parovi)
sub41 = sub41[sub41["hopCount"] >= 50].sort_values("queueLength")

sub41 = sub41.drop_duplicates(subset=["queueLength", "hopCount"])

fig1, ax1 = plt.subplots(figsize=(13, 6))

color_delivery = "#1f77b4"
color_loss = "#d62728"

ax1.set_xlabel("Veličina bafera (Queue Length) [paketi]", fontsize=12)
ax1.set_ylabel("Vjerovatnoća isporuke - Delivery Ratio [%]", fontsize=12, color=color_delivery)
line1, = ax1.plot(sub41["queueLength"], sub41["delivery_ratio"],
                  color=color_delivery, marker="o", linewidth=2, markersize=6,
                  label="Delivery Ratio (%)")
ax1.tick_params(axis="y", labelcolor=color_delivery)
ax1.set_ylim(0, 35)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

ax2 = ax1.twinx()
ax2.set_ylabel("Gubitak paketa - Packet Loss [%]", fontsize=12, color=color_loss)
line2, = ax2.plot(sub41["queueLength"], sub41["packet_loss"],
                  color=color_loss, marker="s", linewidth=2, markersize=6,
                  linestyle="--", label="Packet Loss (%)")
ax2.tick_params(axis="y", labelcolor=color_loss)
ax2.set_ylim(65, 100)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))

# Oznaka maksimuma
max_idx = sub41["delivery_ratio"].idxmax()
ax1.annotate(f"Max: {sub41.loc[max_idx,'delivery_ratio']:.1f}%\n(queueLength={sub41.loc[max_idx,'queueLength']})",
             xy=(sub41.loc[max_idx,"queueLength"], sub41.loc[max_idx,"delivery_ratio"]),
             xytext=(sub41.loc[max_idx,"queueLength"] + 200, sub41.loc[max_idx,"delivery_ratio"] + 3),
             fontsize=10, color=color_delivery,
             arrowprops=dict(arrowstyle="->", color=color_delivery))

lines = [line1, line2]
ax1.legend(lines, [l.get_label() for l in lines], loc="lower right", fontsize=11)


ax_top = ax1.twiny()
ax_top.set_xlim(ax1.get_xlim())
ax_top.set_xticks(sub41["queueLength"])
ax_top.set_xticklabels([f"HC={h}" for h in sub41["hopCount"]], rotation=90, fontsize=7)
ax_top.set_xlabel("Hop Count (HC)", fontsize=10)

plt.title("Podscenarij 4.1 – Uticaj veličine bafera i maksimalnog broja skokova\nna vjerovatnoću isporuke i gubitak paketa (nWifis = 50)",
          fontsize=13, fontweight="bold", pad=30)

ax1.set_xticks(sub41["queueLength"])
ax1.set_xticklabels(sub41["queueLength"], rotation=45, fontsize=8)
plt.grid(True, linestyle="--", alpha=0.4)
fig1.tight_layout()
plt.savefig("scenarij4_1_queue_hop.png", dpi=150)
plt.show()
print("Graf sačuvan kao: scenarij4_1_queue_hop.png")


# Podscenarij 4.2 – nWifis i queueLength (hopCount=50)
sub42 = df[df["hopCount"] == 50].copy()
sub42 = sub42.drop_duplicates(subset=["nWifis", "queueLength"])
sub42 = sub42.sort_values("nWifis")

fig2, ax1 = plt.subplots(figsize=(13, 6))

ax1.set_xlabel("Broj čvorova (nWifis)", fontsize=12)
ax1.set_ylabel("Vjerovatnoća isporuke - Delivery Ratio [%]", fontsize=12, color=color_delivery)
line1, = ax1.plot(sub42["nWifis"], sub42["delivery_ratio"],
                  color=color_delivery, marker="o", linewidth=2, markersize=6,
                  label="Delivery Ratio (%)")
ax1.tick_params(axis="y", labelcolor=color_delivery)
ax1.set_ylim(0, 45)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

ax2 = ax1.twinx()
ax2.set_ylabel("Gubitak paketa - Packet Loss [%]", fontsize=12, color=color_loss)
line2, = ax2.plot(sub42["nWifis"], sub42["packet_loss"],
                  color=color_loss, marker="s", linewidth=2, markersize=6,
                  linestyle="--", label="Packet Loss (%)")
ax2.tick_params(axis="y", labelcolor=color_loss)
ax2.set_ylim(55, 105)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))

max_idx = sub42["delivery_ratio"].idxmax()
ax1.annotate(f"Max: {sub42.loc[max_idx,'delivery_ratio']:.1f}%\n(nWifis={sub42.loc[max_idx,'nWifis']})",
             xy=(sub42.loc[max_idx,"nWifis"], sub42.loc[max_idx,"delivery_ratio"]),
             xytext=(sub42.loc[max_idx,"nWifis"] + 3, sub42.loc[max_idx,"delivery_ratio"] + 3),
             fontsize=10, color=color_delivery,
             arrowprops=dict(arrowstyle="->", color=color_delivery))

ax_top = ax1.twiny()
ax_top.set_xlim(ax1.get_xlim())
ax_top.set_xticks(sub42["nWifis"])
ax_top.set_xticklabels([f"QL={q}" for q in sub42["queueLength"]], rotation=90, fontsize=7)
ax_top.set_xlabel("Queue Length (QL)", fontsize=10)

lines = [line1, line2]
ax1.legend(lines, [l.get_label() for l in lines], loc="upper right", fontsize=11)

plt.title("Podscenarij 4.2 – Uticaj broja čvorova i veličine bafera\nna vjerovatnoću isporuke i gubitak paketa (hopCount = 50)",
          fontsize=13, fontweight="bold", pad=30)

ax1.set_xticks(sub42["nWifis"])
ax1.set_xticklabels(sub42["nWifis"], rotation=45, fontsize=8)
plt.grid(True, linestyle="--", alpha=0.4)
fig2.tight_layout()
plt.savefig("scenarij4_2_nodes_queue.png", dpi=150)
plt.show()
print("Graf sačuvan kao: scenarij4_2_nodes_queue.png")

# Podscenarij 4.3 – nWifis i hopCount (queueLength=1000)
sub43 = df[df["queueLength"] == 1000].copy()
sub43 = sub43.drop_duplicates(subset=["nWifis", "hopCount"])
sub43 = sub43.sort_values("nWifis")

fig3, ax1 = plt.subplots(figsize=(13, 6))

ax1.set_xlabel("Broj čvorova (nWifis)", fontsize=12)
ax1.set_ylabel("Vjerovatnoća isporuke - Delivery Ratio [%]", fontsize=12, color=color_delivery)
line1, = ax1.plot(sub43["nWifis"], sub43["delivery_ratio"],
                  color=color_delivery, marker="o", linewidth=2, markersize=6,
                  label="Delivery Ratio (%)")
ax1.tick_params(axis="y", labelcolor=color_delivery)
ax1.set_ylim(0, 45)
ax1.yaxis.set_major_locator(ticker.MultipleLocator(5))

ax2 = ax1.twinx()
ax2.set_ylabel("Gubitak paketa - Packet Loss [%]", fontsize=12, color=color_loss)
line2, = ax2.plot(sub43["nWifis"], sub43["packet_loss"],
                  color=color_loss, marker="s", linewidth=2, markersize=6,
                  linestyle="--", label="Packet Loss (%)")
ax2.tick_params(axis="y", labelcolor=color_loss)
ax2.set_ylim(55, 105)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(5))

max_idx = sub43["delivery_ratio"].idxmax()
ax1.annotate(f"Max: {sub43.loc[max_idx,'delivery_ratio']:.1f}%\n(nWifis={sub43.loc[max_idx,'nWifis']})",
             xy=(sub43.loc[max_idx,"nWifis"], sub43.loc[max_idx,"delivery_ratio"]),
             xytext=(sub43.loc[max_idx,"nWifis"] + 3, sub43.loc[max_idx,"delivery_ratio"] + 3),
             fontsize=10, color=color_delivery,
             arrowprops=dict(arrowstyle="->", color=color_delivery))

ax_top = ax1.twiny()
ax_top.set_xlim(ax1.get_xlim())
ax_top.set_xticks(sub43["nWifis"])
ax_top.set_xticklabels([f"HC={h}" for h in sub43["hopCount"]], rotation=90, fontsize=7)
ax_top.set_xlabel("Hop Count (HC)", fontsize=10)

lines = [line1, line2]
ax1.legend(lines, [l.get_label() for l in lines], loc="upper right", fontsize=11)

plt.title("Podscenarij 4.3 – Uticaj broja čvorova i maksimalnog broja skokova\nna vjerovatnoću isporuke i gubitak paketa (queueLength = 1000)",
          fontsize=13, fontweight="bold", pad=30)

ax1.set_xticks(sub43["nWifis"])
ax1.set_xticklabels(sub43["nWifis"], rotation=45, fontsize=8)
plt.grid(True, linestyle="--", alpha=0.4)
fig3.tight_layout()
plt.savefig("scenarij4_3_nodes_hop.png", dpi=150)
plt.show()
print("Graf sačuvan kao: scenarij4_3_nodes_hop.png")