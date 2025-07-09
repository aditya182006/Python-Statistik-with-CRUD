import turtle
import time
import os

# --- SETUP ---
screen = turtle.Screen()
screen.bgcolor("skyblue")
screen.title("Animasi Pesawat Realistis")
screen.setup(width=1000, height=600)

# Tambah gambar pesawat
if os.path.exists("plane.gif"):
    screen.addshape("plane.gif")
else:
    print("❗ File 'plane.gif' tidak ditemukan, pakai bentuk segitiga")
    
# Landasan pacu
runway = turtle.Turtle()
runway.hideturtle()
runway.penup()
runway.goto(-500, -150)
runway.pendown()
runway.color("dimgray")
runway.begin_fill()
for _ in range(2):
    runway.forward(1000)
    runway.right(90)
    runway.forward(100)
    runway.right(90)
runway.end_fill()

# Garis-garis di tengah landasan
runway.color("white")
runway.pensize(3)
for i in range(-400, 500, 80):
    runway.penup()
    runway.goto(i, -100)
    runway.pendown()
    runway.forward(40)

# --- Fungsi Gambar Awan ---
def draw_cloud(x, y):
    cloud = turtle.Turtle()
    cloud.hideturtle()
    cloud.penup()
    cloud.goto(x, y)
    cloud.color("white")
    for offset in [0, 20, 40]:
        cloud.begin_fill()
        cloud.goto(x + offset, y)
        cloud.circle(20)
        cloud.end_fill()

# Tambah beberapa awan
draw_cloud(-300, 200)
draw_cloud(-50, 250)
draw_cloud(200, 180)

# Pesawat
plane = turtle.Turtle()
plane.penup()
plane.goto(-450, -100)
plane.setheading(30)
if os.path.exists("plane.gif"):
    plane.shape("plane.gif")
else:
    plane.shape("triangle")
    plane.shapesize(stretch_wid=1.5, stretch_len=3)

# Lepas landas
for _ in range(120):
    plane.forward(3)
    time.sleep(0.01)

# Tampilkan STALL warning
warning = turtle.Turtle()
warning.hideturtle()
warning.penup()
warning.color("red")
warning.goto(0, 200)
warning.write("STALL WARNING!", font=("Arial", 20, "bold"), align="center")
time.sleep(1)
warning.clear()

# Terbang lurus
plane.setheading(0)
for _ in range(80):
    plane.forward(4)
    time.sleep(0.01)

# Knots indikator
knots_display = turtle.Turtle()
knots_display.hideturtle()
knots_display.penup()
knots_display.goto(400, 250)
knots_display.color("black")

for knots in range(150, 301, 50):
    knots_display.clear()
    knots_display.write(f"{knots} Knots", font=("Arial", 14, "bold"), align="center")
    time.sleep(0.4)

# Landing
plane.setheading(-35)
for step in range(120):
    plane.forward(3)
    if step in [20, 40, 60, 80]:
        knots_display.goto(0, 100)
        msg = {20: "50", 40: "40", 60: "30", 80: "RETARD"}[step]
        knots_display.clear()
        knots_display.write(msg, font=("Arial", 20, "bold"), align="center")
        time.sleep(0.5)
        knots_display.clear()
    time.sleep(0.01)

# Mendarat selesai
plane.setheading(0)
plane.forward(30)
knots_display.goto(0, 0)
knots_display.write("Pesawat Mendarat ✈️", font=("Arial", 16, "bold"), align="center")

screen.mainloop()
