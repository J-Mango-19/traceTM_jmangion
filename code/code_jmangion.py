import csv
from collections import deque

def parse_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        machine_name = next(reader)[0]
        string_read = next(reader)[0]
        states = next(reader)[0].split(',')
        alphabet = next(reader)[0].split(',')
        tape_symbols = next(reader)[0].split(',')
        start_state = next(reader)[0]
        accept_state = next(reader)[0]
        reject_state = next(reader)[0]
        transitions = {}
        
        for row in reader:
            if not row:
                continue
            state, char, next_state, write_char, move_dir = row
            transitions.setdefault((state, char), []).append((next_state, write_char, move_dir))
    
    return {
        'name': machine_name,
        'states': states,
        'alphabet': alphabet,
        'tape_symbols': tape_symbols,
        'start_state': start_state,
        'accept_state': accept_state,
        'reject_state': reject_state,
        'transitions': transitions,
        'string_read': string_read  # list of strings to process
    }
def simulate_ntm(machine, input_string, max_depth=None):
    def print_summary():
        print("\n--- Simulation Summary ---")
        print(f"Solution Depth            : {current_depth}")
        print(f"Configurations Explored   : {total_configurations}")
        print(f"Accepted Configurations   : {accepted_configurations}")
        print(f"Rejected Configurations   : {rejected_configurations}")
        print(f"Level of Nondeterminism   : {total_transitions / (non_leaves or 1):.2f}")
        print("\n--- Transition Log ---")
        for log in transition_log:
            print(log)

    print(f"Running Machine: {machine['name']}")
    print(f"Input String   : {input_string}")
    print("\n--- Simulation Started ---")

    start_config = (machine['start_state'], input_string, 0)  # (state, tape, head_pos)
    tree = [[start_config]]
    transitions = machine['transitions']
    accept_state = machine['accept_state']
    reject_state = machine['reject_state']

    # Initialize counters
    total_transitions = non_leaves = total_configurations = 0
    accepted_configurations = rejected_configurations = 0
    transition_log = []
    current_depth = 0

    while tree:
        current_level = tree.pop(0)
        next_level = []
        print(f"\nDepth {current_depth} - {len(current_level)} configurations being explored")

        for state, tape, head_pos in current_level:
            total_configurations += 1

            if state == accept_state:
                accepted_configurations += 1
                print("\n*** String Accepted ***")
                print_summary()
                return current_depth

            if state == reject_state:
                rejected_configurations += 1
                continue

            # Process transitions
            head_char = tape[head_pos] if 0 <= head_pos < len(tape) else '_'
            possible_transitions = transitions.get((state, head_char), [])

            if len(possible_transitions) > 1:
                non_leaves += 1

            for next_state, write_char, move_dir in possible_transitions:
                # Update tape
                new_tape = list(tape)
                if 0 <= head_pos < len(new_tape):
                    new_tape[head_pos] = write_char
                else:
                    new_tape.append(write_char)

                # Update head position
                new_head_pos = head_pos + (1 if move_dir == 'R' else -1)
                next_config = (next_state, ''.join(new_tape), new_head_pos)
                next_level.append(next_config)

                # Log transitions
                transition_log.append(
                    f"({state}, {head_char}) -> ({next_state}, {write_char}, {move_dir})"
                )

            total_transitions += len(possible_transitions)

        if next_level:
            tree.append(next_level)
            current_depth += 1
        else:
            print("\n*** String Rejected ***")
            print_summary()
            return False

        if max_depth and current_depth >= max_depth:
            print("\n*** Max Depth Reached ***")
            print_summary()
            return None

test_file = input('What test file would you like to run?\n')
test_file = f'test/{test_file}'
max_depth = 20

machine = parse_csv(test_file)
string = machine['string_read']

# Iterate over each string and simulate
print(f"Running simulation for: {string}")
result = simulate_ntm(machine, string, max_depth)
print(f"Solution depth for string '{string}': {result}")
