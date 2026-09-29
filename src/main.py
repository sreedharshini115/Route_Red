from collections import deque


# =========================================================
# PASSENGER NODE - LINKED LIST
# =========================================================

class Passenger:

    def __init__(self, passenger_id, name, seat_number):
        self.id = passenger_id
        self.name = name
        self.seat_number = seat_number
        self.next = None


# =========================================================
# BUS CLASS
# =========================================================

class Bus:

    def __init__(self, bus_number, source, destination, total_seats):

        self.bus_number = bus_number
        self.source = source
        self.destination = destination

        # ARRAY - Seat management
        self.seats = [False] * total_seats

        # LINKED LIST - Passenger records
        self.head = None

        # QUEUE - Waiting passengers
        self.waiting_queue = deque()

        # STACK - Cancelled tickets
        self.cancelled_stack = []


# =========================================================
# ARRAY - BUS STORAGE
# =========================================================

buses = [None, None]


# =========================================================
# INPUT VALIDATION - INTEGER
# =========================================================

def read_int(message):

    while True:

        value = input(message).strip()

        try:
            return int(value)

        except ValueError:
            print("Invalid input! Please enter a number.")


# =========================================================
# INPUT VALIDATION - NAME / TEXT
# =========================================================

def read_name(message):

    while True:

        name = input(message).strip()

        if name == "":
            print("Name cannot be empty!")

        elif not all(ch.isalpha() or ch.isspace() for ch in name):
            print("Please enter letters only.")

        else:
            return name


# =========================================================
# CREATE BUSES
# =========================================================

def create_buses():

    buses[0] = Bus(
        "TN01AB1234",
        "Madurai",
        "Chennai",
        5
    )

    buses[1] = Bus(
        "TN02CD5678",
        "Madurai",
        "Coimbatore",
        5
    )


# =========================================================
# MENU
# =========================================================

def show_menu():

    print("\n====================================")
    print("       SMARTBUS RESERVATION SYSTEM")
    print("====================================")

    print("1. View Buses")
    print("2. View Seat Status")
    print("3. Book Ticket")
    print("4. Cancel Ticket")
    print("5. Search Passenger")
    print("6. Display Passengers")
    print("7. Display Waiting List")
    print("8. Cancellation History")
    print("9. Undo Last Cancellation")
    print("10. Sort Passengers")
    print("11. Find Bus Route")
    print("12. Exit")


# =========================================================
# SELECT BUS
# =========================================================

def select_bus():

    print("\n========== SELECT BUS ==========")

    for i in range(len(buses)):

        print(
            f"{i + 1}. "
            f"{buses[i].bus_number} - "
            f"{buses[i].source} to "
            f"{buses[i].destination}"
        )

    choice = read_int(
        f"Enter bus choice (1-{len(buses)}): "
    )

    if choice < 1 or choice > len(buses):

        print("Invalid bus choice!")
        return None

    return buses[choice - 1]


# =========================================================
# 1. VIEW BUSES
# =========================================================

def view_buses():

    print("\n========== BUS DETAILS ==========")

    for i, bus in enumerate(buses):

        print(f"\nBus {i + 1}")

        print("Bus Number :", bus.bus_number)
        print("From       :", bus.source)
        print("To         :", bus.destination)
        print("Total Seats:", len(bus.seats))


# =========================================================
# 2. VIEW SEATS
# =========================================================

def view_seats():

    bus = select_bus()

    if bus is None:
        return

    print(
        f"\n===== SEATS OF {bus.bus_number} ====="
    )

    for i in range(len(bus.seats)):

        if bus.seats[i]:

            print(f"Seat {i + 1} - Booked")

        else:

            print(f"Seat {i + 1} - Available")


# =========================================================
# CHECK DUPLICATE PASSENGER ID
# =========================================================

def passenger_exists(bus, passenger_id):

    current = bus.head

    while current is not None:

        if current.id == passenger_id:
            return True

        current = current.next

    return False


# =========================================================
# ADD PASSENGER TO LINKED LIST
# =========================================================

def add_passenger(bus, new_passenger):

    if bus.head is None:

        bus.head = new_passenger

    else:

        current = bus.head

        while current.next is not None:
            current = current.next

        current.next = new_passenger


# =========================================================
# 3. BOOK TICKET
# =========================================================

def book_ticket():

    bus = select_bus()

    if bus is None:
        return

    passenger_id = read_int(
        "Enter Passenger ID: "
    )

    if passenger_id <= 0:

        print("Passenger ID must be positive.")
        return

    name = read_name(
        "Enter Passenger Name: "
    )

    # Check duplicate passenger ID

    if passenger_exists(bus, passenger_id):

        print("Passenger ID already exists!")
        return

    seat = read_int(
        "Enter Seat Number: "
    )

    # Check seat number

    if seat < 1 or seat > len(bus.seats):

        print("Invalid seat number!")
        return

    # Check if seat is booked

    if bus.seats[seat - 1]:

        print("\nSeat already booked!")

        waiting = Passenger(
            passenger_id,
            name,
            -1
        )

        # QUEUE
        bus.waiting_queue.append(waiting)

        print(
            f"{name} has been added to the waiting list."
        )

        return

    # Book seat

    bus.seats[seat - 1] = True

    new_passenger = Passenger(
        passenger_id,
        name,
        seat
    )

    # LINKED LIST
    add_passenger(bus, new_passenger)

    print("\nTicket booked successfully!")

    print("Passenger :", name)
    print("Seat      :", seat)
    print("Bus       :", bus.bus_number)


# =========================================================
# REMOVE PASSENGER FROM LINKED LIST
# =========================================================

def remove_passenger(bus, seat):

    current = bus.head
    previous = None

    while current is not None:

        if current.seat_number == seat:

            if previous is None:

                bus.head = current.next

            else:

                previous.next = current.next

            current.next = None

            return current

        previous = current
        current = current.next

    return None


# =========================================================
# 4. CANCEL TICKET
# =========================================================

def cancel_ticket():

    bus = select_bus()

    if bus is None:
        return

    seat = read_int(
        "Enter seat number to cancel: "
    )

    if seat < 1 or seat > len(bus.seats):

        print("Invalid seat number!")
        return

    if not bus.seats[seat - 1]:

        print("Seat is not booked!")
        return

    passenger = remove_passenger(
        bus,
        seat
    )

    if passenger is not None:

        bus.seats[seat - 1] = False

        # STACK
        bus.cancelled_stack.append(passenger)

        print("\nTicket cancelled successfully!")

        print(
            "Passenger:",
            passenger.name
        )

        # QUEUE

        if len(bus.waiting_queue) > 0:

            waiting = bus.waiting_queue.popleft()

            waiting.seat_number = seat

            bus.seats[seat - 1] = True

            add_passenger(
                bus,
                waiting
            )

            print(
                f"\nWaiting passenger "
                f"{waiting.name} received Seat {seat}"
            )


# =========================================================
# 5. LINEAR SEARCH
# =========================================================

def search_passenger():

    bus = select_bus()

    if bus is None:
        return

    passenger_id = read_int(
        "Enter Passenger ID to search: "
    )

    current = bus.head

    # LINEAR SEARCH

    while current is not None:

        if current.id == passenger_id:

            print(
                "\n========== PASSENGER FOUND =========="
            )

            print("ID   :", current.id)
            print("Name :", current.name)
            print("Seat :", current.seat_number)

            return

        current = current.next

    print("Passenger not found!")


# =========================================================
# 6. DISPLAY PASSENGERS
# =========================================================

def display_passengers():

    bus = select_bus()

    if bus is None:
        return

    current = bus.head

    print(
        "\n========== PASSENGER LIST =========="
    )

    if current is None:

        print("No passengers.")
        return

    while current is not None:

        print(
            f"ID: {current.id} | "
            f"Name: {current.name} | "
            f"Seat: {current.seat_number}"
        )

        current = current.next


# =========================================================
# 7. WAITING QUEUE
# =========================================================

def display_waiting_list():

    bus = select_bus()

    if bus is None:
        return

    print(
        "\n========== WAITING LIST =========="
    )

    if len(bus.waiting_queue) == 0:

        print("Waiting list is empty.")
        return

    # QUEUE

    for passenger in bus.waiting_queue:

        print(
            f"ID: {passenger.id} | "
            f"Name: {passenger.name}"
        )


# =========================================================
# 8. CANCELLATION STACK
# =========================================================

def display_cancellation_history():

    bus = select_bus()

    if bus is None:
        return

    print(
        "\n====== CANCELLATION HISTORY ======"
    )

    if len(bus.cancelled_stack) == 0:

        print("No cancellations.")
        return

    # STACK - display from top

    for passenger in reversed(
        bus.cancelled_stack
    ):

        print(
            f"ID: {passenger.id} | "
            f"Name: {passenger.name} | "
            f"Seat: {passenger.seat_number}"
        )


# =========================================================
# 9. UNDO CANCELLATION
# =========================================================

def undo_cancellation():

    bus = select_bus()

    if bus is None:
        return

    if len(bus.cancelled_stack) == 0:

        print("No cancellation to undo.")
        return

    # STACK - POP

    passenger = bus.cancelled_stack.pop()

    seat_index = passenger.seat_number - 1

    if seat_index < 0 or seat_index >= len(bus.seats):

        print("Invalid original seat.")
        return

    if not bus.seats[seat_index]:

        bus.seats[seat_index] = True

        add_passenger(
            bus,
            passenger
        )

        print("\nCancellation undone!")

        print(
            "Passenger:",
            passenger.name
        )

        print(
            "Seat:",
            passenger.seat_number
        )

    else:

        print(
            "Original seat is already occupied."
        )


# =========================================================
# 10. BUBBLE SORT
# =========================================================

def sort_passengers():

    bus = select_bus()

    if bus is None:
        return

    # Convert Linked List to Python List

    passengers = []

    current = bus.head

    while current is not None:

        passengers.append(current)

        current = current.next

    if len(passengers) < 2:

        print(
            "Not enough passengers to sort."
        )

        return

    # BUBBLE SORT BY NAME

    n = len(passengers)

    for i in range(n - 1):

        for j in range(n - i - 1):

            if (
                passengers[j].name.lower()
                >
                passengers[j + 1].name.lower()
            ):

                passengers[j], passengers[j + 1] = (
                    passengers[j + 1],
                    passengers[j]
                )

    print(
        "\n======= SORTED PASSENGERS ======="
    )

    for passenger in passengers:

        print(
            f"ID: {passenger.id} | "
            f"Name: {passenger.name} | "
            f"Seat: {passenger.seat_number}"
        )


# =========================================================
# ADD GRAPH EDGE
# =========================================================

def add_route(graph, city1, city2):

    if city1 not in graph:
        graph[city1] = []

    if city2 not in graph:
        graph[city2] = []

    # Undirected graph

    graph[city1].append(city2)
    graph[city2].append(city1)


# =========================================================
# FIND CITY
# =========================================================

def find_city(graph, city):

    for existing_city in graph:

        if existing_city.lower() == city.lower():

            return existing_city

    return None


# =========================================================
# 11. GRAPH + BFS
# =========================================================

def find_route():

    start = read_name(
        "Enter starting city: "
    )

    destination = read_name(
        "Enter destination city: "
    )

    # GRAPH

    graph = {}

    add_route(
        graph,
        "Madurai",
        "Trichy"
    )

    add_route(
        graph,
        "Trichy",
        "Chennai"
    )

    add_route(
        graph,
        "Madurai",
        "Dindigul"
    )

    add_route(
        graph,
        "Dindigul",
        "Coimbatore"
    )

    add_route(
        graph,
        "Chennai",
        "Pondicherry"
    )

    # Convert city names to standard form

    start_city = find_city(
        graph,
        start
    )

    destination_city = find_city(
        graph,
        destination
    )

    if (
        start_city is None
        or
        destination_city is None
    ):

        print(
            "City not available in route map."
        )

        return

    # BFS QUEUE

    queue = deque()

    visited = set()

    parent = {}

    queue.append(start_city)

    visited.add(start_city)

    # BFS

    while queue:

        current = queue.popleft()

        if current == destination_city:
            break

        for neighbour in graph.get(
            current,
            []
        ):

            if neighbour not in visited:

                visited.add(neighbour)

                queue.append(neighbour)

                parent[neighbour] = current

    if destination_city not in visited:

        print("No route found.")
        return

    # STACK - Build route backwards

    route = []

    current = destination_city

    while current is not None:

        route.append(current)

        current = parent.get(current)

    # Reverse stack result

    route.reverse()

    print(
        "\n========== BUS ROUTE =========="
    )

    print(
        " -> ".join(route)
    )


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    create_buses()

    while True:

        show_menu()

        choice = read_int(
            "Enter your choice: "
        )

        if choice == 1:

            view_buses()

        elif choice == 2:

            view_seats()

        elif choice == 3:

            book_ticket()

        elif choice == 4:

            cancel_ticket()

        elif choice == 5:

            search_passenger()

        elif choice == 6:

            display_passengers()

        elif choice == 7:

            display_waiting_list()

        elif choice == 8:

            display_cancellation_history()

        elif choice == 9:

            undo_cancellation()

        elif choice == 10:

            sort_passengers()

        elif choice == 11:

            find_route()

        elif choice == 12:

            print(
                "\nThank you for using "
                "SmartBus Reservation System!"
            )

            break

        else:

            print(
                "Invalid choice! "
                "Please select 1-12."
            )


# =========================================================
# PROGRAM START
# =========================================================

if __name__ == "__main__":
    main()
