from queue import PriorityQueue

def find_escape_path(grid, start_pos, room_positions):
    """Find the escape path from start position to an exit and return directions."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    start_row, start_col = start_pos

    # Initialize priority queue and visited set
    pq = PriorityQueue()
    pq.put((0, start_row, start_col))
    visited = set()
    
    # Keep track of the parent of each cell for reconstructing the path
    parent = {}
    parent[(start_row, start_col)] = None

    while not pq.empty():
        cost, row, col = pq.get()
        
        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Check if we've reached an exit (edge of the grid)
        if row == 0 or row == len(grid)-1 or col == 0 or col == len(grid[0])-1:
            path = []
            directions_path = []
            while parent[(row, col)] is not None:
                prev_row, prev_col = parent[(row, col)]
                path.append((row, col))
                
                # Adding directions to the path
                if row - prev_row == 1:
                    directions_path.append("Go Down")
                elif row - prev_row == -1:
                    directions_path.append("Go Up")
                elif col - prev_col == 1:
                    directions_path.append("Go Right")
                elif col - prev_col == -1:
                    directions_path.append("Go Left")
                
                row, col = prev_row, prev_col

            path.append((start_row, start_col))
            path.reverse()
            directions_path.reverse()
            
            # Convert path from coordinates to room names
            directions_in_rooms = []
            for direction, position in zip(directions_path, path):
                row, col = position
                room_name = get_room_name_at_position(room_positions, row, col)
                directions_in_rooms.append(f"{direction} to {room_name}")
            
            return directions_in_rooms

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and (new_row, new_col) not in visited:
                pq.put((cost + 1, new_row, new_col))
                parent[(new_row, new_col)] = (row, col)

    return ["No escape path found"]

def get_room_name_at_position(room_positions, row, col):
    """Get the room name at a specific position (row, col)."""
    for room, position in room_positions.items():
        if position == (row, col):
            return room
    return "Unknown Room"
