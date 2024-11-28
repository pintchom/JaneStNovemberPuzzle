from math import pi, sqrt, acos, sin

def get_area(point: tuple[int, int]) -> int:
    # print(f"Trying {point}")
    base1 = 1 - point[0]
    base2 = point[0]
    height = point[1]
    radius1 = sqrt(base1**2 + height**2)
    radius2 = sqrt(base2**2 + height**2)
    C1 = (pi * radius1**2)/4
    # print(f"left side circle area: {C1}")
    C2 = (pi * radius2**2)/4
    # print(f"right side circle area: {C2}")
    
    # Calculate intersection area using circle intersection formula
    d = sqrt((base2 - base1)**2 + (0 - 0)**2)  # Distance between circle centers
    
    # Calculate intersection area only within 1x1 square bounds
    if d >= radius1 + radius2:  # No intersection
        intersection = 0
    elif d <= abs(radius1 - radius2):  # One circle contains the other
        # Only count intersection within square bounds
        intersection = min(pi * min(radius1, radius2)**2 / 4, 1.0)
    else:
        # Formula for intersection area of two circles
        a = 2 * acos((d**2 + radius1**2 - radius2**2)/(2*d*radius1))
        b = 2 * acos((d**2 + radius2**2 - radius1**2)/(2*d*radius2))
        # Only count 1/4 of the intersection since we're using quarter circles
        intersection = (0.5 * radius1**2 * (a - sin(a)) +
                       0.5 * radius2**2 * (b - sin(b))) / 4
    
    # Total area is sum of quarter circles minus bounded intersection
    total_area = C1 + C2 - intersection
    return total_area


areas = []
# 0.5 is 5000000000 in terms of 0.0000000001 steps
# print('Loading...')
# for i in range(5000000001):
#     # Only go up to i to maintain triangular pattern
#     for j in range(i + 1):
#         try:
#             x = i * 0.0000000001
#             y = j * 0.0000000001
#             area = get_area((x, y))
#             areas.append(area)
#         except ValueError:
#             # Skip points that cause math domain errors
#             continue

# Try 1 million random points in triangle
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Lists to store coordinates and areas
xs = []
ys = []
areas = []

for _ in range(10000000000):  # Reduced points for plotting
    # Generate random point in triangle
    x = random.random() * 0.5  # x from 0 to 0.5
    y = random.random() * x    # y from 0 to x to maintain triangle shape
    try:
        area = get_area((x, y))
        xs.append(x)
        ys.append(y)
        areas.append(area)
    except ValueError:
        # Skip points that cause math domain errors
        continue

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot points colored by area
scatter = ax.scatter(xs, ys, areas, c=areas, cmap='viridis')
plt.colorbar(scatter, label='Area')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Area')
ax.set_title('Area Distribution Over Triangle Domain')

plt.show()

print(f"Average area: {sum(areas)/len(areas)}")

'''
0.00, 0.00
0.01, 0.00 -> 0.01, 0.01
0.02, 0.00 -> 0.02, 0.01 -> 0.02, 0.02
0.03, 0.00 -> 0.03, 0.01 -> 0.03, 0.02 -> 0.03, 0.03
0.04, 0.00 -> 0.04, 0.01 -> 0.04, 0.02 -> 0.04, 0.03 -> 0.04, 0.04
0.05, 0.00 -> 0.05, 0.01 -> 0.05, 0.02 -> 0.05, 0.03 -> 0.05, 0.04 -> 0.05, 0.05
'''

