from idlelib.colorizer import color_config

rgb = [256, 0, 0]
def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"
def rainbow_hex():
    for i in range(256):
        rgb[1] += 1
    


import matplotlib.pyplot as plt

activities = ["Swimming", "Gym", "Yoga", "Football", "Badminton"]
bookings = [38, 65, 22, 47, 31]

# TODO 1: Create a bar chart with plt.bar().
plt.bar(activities, bookings, color="#b4a3d7")
# TODO 2: Add a title and labels.
plt.title("Sports Centre Bookings")
plt.xlabel("Activities")
plt.ylabel("Number Of Bookings")
# TODO 3: Show the chart.
plt.show()