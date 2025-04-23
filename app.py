from flask import Flask, render_template, request, redirect, url_for
import random
from queue import PriorityQueue

app = Flask(__name__)

# Define room names and their positions in a 10x10 grid
room_names = [
    "Classroom A", "Classroom B", "Classroom C", "Classroom D", "Classroom E",
    "Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 5",
    "Hallway 1", "Hallway 2", "Hallway 3", "Hallway 4", "Hallway 5",
    "Office A", "Office B", "Office C", "Office D", "Office E",
    "Lobby A", "Lobby B", "Lobby C", "Lobby D", "Lobby E"
]

grid = [[None for _ in range(10)] for _ in range(10)]
room_positions = {}
index = 0
for i in range(10):
    for j in range(10):
        if index < len(room_names):
            room = room_names[index]
            grid[i][j] = room
            room_positions[room] = (i, j)
            index += 1
        else:
            grid[i][j] = ""

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("dashboard"))
    return render_template("login.html")

# @app.route("/dashboard")
# def dashboard():
#     return render_template("select_location.html", rooms=list(room_positions.keys()))

@app.route("/dashboard")
def dashboard():
    return render_template("select_location.html", rooms=list(room_positions.keys()))


# @app.route("/result", methods=["POST"])
# def result():
#     start_room = request.form["select_location"]
#     fire_rooms = random.sample(list(room_positions.keys()), 5)
#     start_pos = room_positions[start_room]
#     path = find_escape_path(grid, start_pos, room_positions, fire_rooms)
#     directions = path_to_directions(path, grid)
#     return render_template("result.html", start=start_room, fire_rooms=fire_rooms, directions=directions)

@app.route("/result", methods=["POST"])
def result():
    start_room = request.form["select_location"]  # This should match the form's 'name'
    fire_rooms = random.sample(list(room_positions.keys()), 5)
    start_pos = room_positions[start_room]
    path = find_escape_path(grid, start_pos, room_positions, fire_rooms)
    directions = path_to_directions(path, grid)
    ##
    # Build a grid visualization
    visual_grid = []
    for i in range(10):
        row = []
        for j in range(10):
            cell = ""
            room = grid[i][j]
            pos = (i, j)

            if room in fire_rooms:
                cell = "fire"
            elif pos == room_positions[start_room]:
                cell = "start"
            elif pos in path:
                cell = "path"
            else:
                cell = "safe"

            row.append(cell)
        visual_grid.append(row)

   # return render_template("result.html", start=start_room, fire_rooms=fire_rooms, directions=directions)
    #return render_template("result.html", start=start_room, fire_rooms=fire_rooms, directions=directions, path=path, grid=grid)
    return render_template("result.html", start=start_room, fire_rooms=fire_rooms, directions=directions, grid=visual_grid)





def find_escape_path(grid, start_pos, room_positions, fire_rooms):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    exit_rooms = ['Lobby A', 'Lobby B', 'Office D']
    valid_exits = [room_positions[room] for room in exit_rooms if room in room_positions and room not in fire_rooms]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(start, goal):
        queue = PriorityQueue()
        queue.put((0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while not queue.empty():
            _, current = queue.get()

            if current == goal:
                break

            for dx, dy in directions:
                nx, ny = current[0] + dx, current[1] + dy
                next_cell = (nx, ny)
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                    room = grid[nx][ny]
                    if room and room not in fire_rooms:
                        new_cost = cost_so_far[current] + 1
                        if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                            cost_so_far[next_cell] = new_cost
                            priority = new_cost + heuristic(goal, next_cell)
                            queue.put((priority, next_cell))
                            came_from[next_cell] = current

        path = []
        if goal in came_from:
            current = goal
            while current != start:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
        return path

    for exit_pos in valid_exits:
        path = a_star(start_pos, exit_pos)
        if path:
            return path

    return []



def path_to_directions(path, grid):
    directions = []
    for i in range(1, len(path)):
        prev = path[i - 1]
        curr = path[i]
        dx, dy = curr[0] - prev[0], curr[1] - prev[1]

        if dx == -1:
            move = "Up"
        elif dx == 1:
            move = "Down"
        elif dy == -1:
            move = "Left"
        elif dy == 1:
            move = "Right"
        else:
            move = "Stay"

        room_name = grid[curr[0]][curr[1]] or "Empty Space"
        directions.append(f"Go {move} to {room_name}")
    return directions


if __name__ == "__main__":
    app.run(debug=True)
