import sys
from math import inf

def z_array(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            l, r = i, i + z[i]
            z[i] += 1
    return z

def pi_from_z(z):
    """
    convert Z values to  array pi, where
    basically we are getting pi[t] = length of longest proper prefix of s[:t+1] that is also its suffix.
    time complexity O(n): each pi position is assigned at most once.
    """
    n = len(z)
    pi = [0] * n
    for i in range(1, n):
        k = z[i]
        # we start from k = z[i] and assign descending lengths to the segment [i, i+k-1]
        # stopping when a position already has a value.
        while k > 0:
            pos = i + k - 1
            if pi[pos] == 0:
                pi[pos] = k
                k -= 1
            else:
                break
    return pi

def preprocess_extended_bad_character(pat):
    """
    preprocess bad-character table for reverse BM.
    rather than get the rightmost index of the mismatched character to the left of pat, we get the leftmost index to the right of the mismatch
    since we scan left to right.
    table[c][j] = leftmost index of c in pat[j+1:], or -1 if none.
    """
    m = len(pat)
    chars = set(pat)
    table = {c: [-1] * (m + 1) for c in chars}
    next_pos = {c: -1 for c in chars}
    for j in range(m - 1, -1, -1):
        for c in chars:
            table[c][j] = next_pos[c]
        next_pos[pat[j]] = j
    return table

def preprocess_good_prefix(pat):
    """
    we get the good-prefix shifts for reverse BM instead of the good suffix shifts since we scan left to right
    gp[j] for j in [0..m]. If the matched prefix of length j reoccurs at some start p>=1 (Z[p] >= j), then shift = minimal such p.
    else we fallback to border of prefix j: shift = max(1, j - border_len(j)).
    for full match (j == m): shift by period = m - longest_border(pat).
    """
    m = len(pat)
    if m == 0:
        return [1]
    z = z_array(pat)

    # Minimal start p for a reoccurrence of each prefix length
    bestShift = [inf] * (m + 1)
    for p in range(1, m):
        L = z[p]
        if L > 0 and bestShift[L] > p:
            bestShift[L] = p
    # Make usable for smaller lengths too
    for L in range(m - 1, 0, -1):
        if bestShift[L] > bestShift[L + 1]:
            bestShift[L] = bestShift[L + 1]

    # we get the border lengths from the Z-array
    pi = pi_from_z(z)

    def border_len(prefix_len):
        if prefix_len == 0:
            return 0
        return pi[prefix_len - 1]

    gp = [1] * (m + 1)
    for j in range(1, m):
        if bestShift[j] != inf:
            gp[j] = bestShift[j]
        else:
            k = border_len(j)
            gp[j] = max(1, j - k)

    # full match shift =  the length of the entire period
    gp[m] = m - border_len(m) if m > 0 else 1
    gp[0] = 1
    return gp


def reverse_boyer_moore(txt, pat):
    """
    Reverse Boyer-Moore:
    align pat at s = n - m and compare j=0..m-1 (left->right).
    on mismatch at j with text char c:
    we get bad-char shift = (k - j) if c occurs at k>j in pat else (m - j)
    and good-prefix shift = gp[j] (or 1 when j==0)
    then we shift left by max of the two (>=1).
    on full match: shift by gp[m].
    return 1-based indexing match positions.
    """
    n, m = len(txt), len(pat)
    if m == 0 or n == 0 or m > n:
        return []

    # we preprocess the shifts by calling the respective functions
    bc = preprocess_extended_bad_character(pat)
    gp = preprocess_good_prefix(pat)

    matches = []
    s = n - m  # we start at the right end of text

    while s >= 0:
        j = 0
        while j < m and pat[j] == txt[s + j]:
            j += 1

        if j == m:
            matches.append(s + 1)         # 1-based indexing for output so we add 1
            shift = gp[m]
            s -= shift if shift > 0 else 1
            continue

        c = txt[s + j]

        # we calculate the bad character shift
        if c in bc:
            k = bc[c][j]                  # leftmost in pat[j+1:]
            bc_shift = (k - j) if k != -1 else (m - j)
        else:
            bc_shift = (m - j)

        # calculate good prefix shift
        gs_shift = gp[j] if j > 0 else 1

        # we shift the pat leftwards along the text by the max of the 2 shifts
        s -= max(1, bc_shift, gs_shift)

    return matches

def main():
    if len(sys.argv) != 3:
        print("Usage: python a1q2.py <text_filename> <pattern_filename>")
        sys.exit(1)

    text_file, pattern_file = sys.argv[1], sys.argv[2]
    try:
        with open(text_file, 'r') as f:
            txt = f.read().strip()
        with open(pattern_file, 'r') as f:
            pat = f.read().strip()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    matches = reverse_boyer_moore(txt, pat)

    with open('output_a1q2.txt', 'w') as f:
        for pos in matches:
            f.write(f"{pos}\n")

    print(f"Found {len(matches)} matches. Results written to output_a1q2.txt")

if __name__ == "__main__":
    main()
