import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles

days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
visitors = [42, 55, 48, 63, 80]



plt.plot(days, visitors, marker="s", linestyle="--")
plt.title("Weekly Visitor Numbers")
plt.xlabel("Day")
plt.ylabel("Number of visitors")
plt.grid(True)
plt.tight_layout()
plt.show()
