import consts
from itertools import product, combinations, permutations
from cleartext_criteria import *

def main(args):
    cyphertext_file = args.file
    top = args.top
    clearfile = args.clearfile
    print(f"Using {clearfile} as a sample...")

    # get some frequencies
    with open(clearfile, 'rt', encoding='utf-8') as f:
        text = normalize_string(f.read(), ALPHABET, TRANSLATOR)
        bg_freq = ngram_frequencies(
            text=text,
            n=2,
            overlap=False
        )
        mg_freq = ngram_frequencies(text, 1, True)
        e = entropy_from_probabilities(mg_freq.values())
        print(f"Sample text entropy: {e}")

    # get some cyphertext
    with open(cyphertext_file, 'rt', encoding='utf-8') as f:
        ct_norm = normalize_string(
            f.read(), consts.ALPHABET, consts.TRANSLATOR)
        ct_bg_freq = ngram_frequencies(ct_norm, n=2, overlap=False)

    # sort by descending frequencies
    bgf_sorted = sort_fqs(bg_freq)

    # use known bgs?
    if args.ukb:
        print(f"Prioritising these known top 5 cleartext bigrams:", MOST_FREQUENT_BG)
        bgf_sorted = MOST_FREQUENT_BG + bgf_sorted

    ct_bgf_sorted = sort_fqs(ct_bg_freq)

    print(f"Top {top} cleartext bigrams (actually considered):",
          bgf_sorted[:top])
    print(f"Top {top} cyphertext bigrams:", ct_bgf_sorted[:top])

    key_candidates: Set[Tuple[int, int]] = set()
    m = len(ALPHABET) ** 2
    for pair_ct, pair_t in product(combinations(ct_bgf_sorted[:top], 2), permutations(bgf_sorted[:top], 2)):
        x1, x2 = bg_to_num(pair_t[0]), bg_to_num(pair_t[1])
        y1, y2 = bg_to_num(pair_ct[0]), bg_to_num(pair_ct[1])
        s = solve_congruence(
            x1-x2, y1-y2, m
        )
        if len(s) > 0:
            for s in s:
                b = (y1-s*x1) % m
                if abs(gcd(s, m)) == 1:
                    key_candidates.add((s, b))

    print("Total candidates:", len(key_candidates))

    print("Trying to reduce the number by running a few tests...")
    # now we try to reduce the number of possibly valid keys
    decs = []
    false_keys = set()
    for key in key_candidates:
        dec = decrypt(ct_norm, key=key)
        letter_freq = ngram_frequencies(dec, 1, False)
        if not check_entropy(dec, letter_freq, args.e)\
                or not check_letter_min_freq(dec, letter_freq, mg_freq, args.n, args.q):
            false_keys.add(key)
            continue

        decs.append(dec)

    key_candidates = key_candidates - false_keys

    print("Keys remaining:", len(key_candidates))

    if len(key_candidates) < 11:
        for key in key_candidates:
            dec = decrypt(ct_norm, key)
            letter_freq = ngram_frequencies(dec, 1, False)
            e = entropy_from_probabilities(letter_freq.values())
            print(f"Key: {key}")
            print(dec, "\n\n")
            print(f"Actual entropy per character: {e}")
            print(f"Actual top letter frequencies: {list(map(lambda x: (x[0], '%.3f%%' %( 100*x[1])), sort_fqs_val(letter_freq)[:10]))}")
    else:
        print("Stil more than 10 keys remaining... Not good.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, help="file of cyphertext")
    parser.add_argument("clearfile", type=str,
                        help="file which will be used as a sample for frequency analysis")
    parser.add_argument("--top", type=int, default=5, dest="top",
                        help="how many most frequent bigrams should be checked")
    parser.add_argument("--use-known-bigrams", action='store_true', dest='ukb',
                        help="whether to use known top 5 most frequent bigrams (will be included in total --top count, before the ones sampled from clearfile)")
    parser.add_argument("-q", default=0.7, type=float, help="min freq multiplier")
    parser.add_argument("-n", default=5, type=int, help="min letters to check")
    parser.add_argument("-e", default=4.9, type=float, help="max cleartext entropy")
    args = parser.parse_args()
    main(args)
