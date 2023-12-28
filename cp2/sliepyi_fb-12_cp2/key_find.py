def read_text_from_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def calculate_coincidence_index(text):
    letter_count = {}
    block_length = len(text)

    for char in text:
        if char.isalpha():
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1

    coincidence_sum = sum(count * (count - 1) for count in letter_count.values())
    index_of_coincidence = coincidence_sum / (block_length * (block_length - 1))

    return index_of_coincidence

def split_text_into_blocks(text, key_length):
    blocks = ['' for _ in range(key_length)]
    for i, char in enumerate(text):
        block_index = i % key_length
        blocks[block_index] += char
    return blocks

def find_key(message, key_length):
    blocks = split_text_into_blocks(message, key_length)
    key = ''
    for block in blocks:
        most_common = max(block, key=block.count)
        key += chr(((ord(most_common) - ord('о')) % 32+1072))
    return key

if __name__ == "__main__":
    key_length = 17
    message = read_text_from_file("variant.txt")

    # Calculate the average IC for each block
    blocks = split_text_into_blocks(message, key_length)
    ics = [calculate_coincidence_index(block) for block in blocks]
    average_ic = sum(ics) / key_length

    # Find the key
    key = find_key(message, key_length)

    print(f"Decoded key: {key}")
