string1 = "12345678"
string2 = "123"

repeat_count = len(string1) // len(string2)

# Repeat string2 as many times as possible
string2_repeated = string2 * repeat_count

# Append part of string2 to match the length of string1
string2_repeated += string2[:len(string1) - len(string2_repeated)]

print(string2_repeated)