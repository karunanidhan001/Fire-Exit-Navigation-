import random

ROOM_NAMES = [
    'Classroom A', 'Classroom B', 'Classroom C', 'Classroom D', 'Classroom E',
    'Lab 1', 'Lab 2', 'Lab 3', 'Office 1', 'Office 2', 'Lobby 1', 'Lobby 2', 'Hallway 1', 'Hallway 2'
]

def generate_map(start_room):
    """Generate the 10x10 grid map and return it with positions of rooms."""
    grid = [['' for _ in range(10)] for _ in range(10)]
    room_positions = {}

    rooms = ROOM_NAMES + [start_room]  # Including the start room
    random.shuffle(rooms)

    for idx, room in enumerate(rooms):
        row, col = divmod(idx, 10)
        grid[row][col] = room
        room_positions[room] = (row, col)

    return grid, room_positions[start_room], room_positions

def generate_random_fire(room_positions, count=5):
    """Randomly select rooms to catch fire."""
    fire_rooms = random.sample(list(room_positions.keys()), count)
    return fire_rooms
