def read(output_file):
    with open(output_file, 'r', encoding='utf-8') as file:
        message = file.read()
    return message

def calculate_coincidence_index(block):
    letter_count = {}
    block_length = len(block)

    for char in block:
        if char.isalpha():
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1

    coincidence_sum = sum(count * (count - 1) for count in letter_count.values())
    index_of_coincidence = coincidence_sum / (block_length * (block_length - 1))

    return index_of_coincidence

message = read("variant.txt")
results = {}

target_ic = 0.0467558  #Target IC value to find the closest match
closest_ic_diff = float('inf') 
closest_ic_key_length = None

for key_length in range(2, 31):
    blocks = [[] for _ in range(key_length)]
    ics = []

    for i, char in enumerate(message):
        block_index = i % key_length
        blocks[block_index].append(char)

    for i, block in enumerate(blocks, start=1):
        ic = calculate_coincidence_index(''.join(block))
        ics.append(ic)

    average_ic = sum(ics) / key_length
    results[key_length] = average_ic

    ic_diff = abs(average_ic - target_ic)
    if ic_diff < closest_ic_diff:
        closest_ic_diff = ic_diff
        closest_ic_key_length = key_length

for key_length, average_ic in results.items():
    print(f"Key Length: {key_length}, Average IC: {average_ic:.12f}")

print(f"Key Length closest to {target_ic}: {closest_ic_key_length}, Average IC: {results[closest_ic_key_length]:.12f}")