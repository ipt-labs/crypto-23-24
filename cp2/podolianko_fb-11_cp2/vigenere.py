def encrypt(msg: str, key: str, alpha: str) -> str:
    clear_as_idx = [alpha.find(m) for m in msg]
    key_as_idx = [alpha.find(k) for k in key]
    key_i_len, clear_i_len, alpha_len = len(
        key_as_idx), len(clear_as_idx), len(alpha)

    cypher = [alpha[(clear_as_idx[i] + key_as_idx[i % key_i_len]) % alpha_len]
              for i in range(clear_i_len)]
    return ''.join(cypher)


def decrypt(cypher: str, key: str, alpha: str) -> str:
    cypher_as_idx = [alpha.find(c) for c in cypher]
    key_as_idx = [alpha.find(k) for k in key]
    key_i_len, cypher_i_len, alpha_len = len(
        key_as_idx), len(cypher), len(alpha)

    clear = [alpha[(cypher_as_idx[i] - key_as_idx[i % key_i_len]) % alpha_len]
             for i in range(cypher_i_len)]
    return ''.join(clear)