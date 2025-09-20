#!/usr/bin/env python3
"""
Reverse Boyer-Moore algorithm implementation with both extended bad character
and good suffix rules. Pattern shifts leftwards, scanning from left to right.
Uses the rule that gives the largest shift.
"""

import sys

def preprocess_extended_bad_character(pat):
    """
    Precompute extended bad character table for O(1) lookups.
    Returns the table where table[c][j] = leftmost occurrence of the mismatched character in pat[j+1:]
    """
    m = len(pat)
    chars = set(pat)
    table = {c: [-1] * (m + 1) for c in chars}

    # For each character, track its next occurrence as we scan left to right
    next_pos = {c: -1 for c in chars}

    for j in range(m - 1, -1, -1):
        for c in chars:
            table[c][j] = next_pos[c]
        next_pos[pat[j]] = j

    return table


def preprocess_good_prefix(pat):
    """
    Preprocess good suffix (but in this case since we do reverse it is actually the prefix) shift table for reverse Boyer-Moore.
    Returns an array where good_prefix[i] is the shift distance when
    a prefix of length i has been matched.
    """
    m = len(pat)
    good_prefix = [0] * (m + 1)
    
    # Case 1: The matched prefix appears elsewhere in the pattern
    # Precompute the border array (fundamental preprocessing)
    border = [0] * (m + 1)
    i, j = m, m + 1
    border[i] = j
    
    while i > 0:
        while j <= m and pat[i - 1] != pat[j - 1]:
            if good_prefix[j] == 0:
                good_prefix[j] = j - i
            j = border[j]
        i -= 1
        j -= 1
        border[i] = j
    
    # Case 2: Only part of the matched prefix appears at the end
    j = border[0]
    for i in range(0, m + 1):
        if good_prefix[i] == 0:
            good_prefix[i] = j
        if i == j:
            j = border[j]
    
    return good_prefix

def reverse_boyer_moore(txt, pat):
    """
    Reverse Boyer-Moore algorithm with both extended bad character
    and good suffix rules. Shifts pattern leftwards, scans left to right.
    Uses the rule that gives the largest shift.
    Includes debug output for shift decisions and jump count.
    """
    n, m = len(txt), len(pat)
    matches = []
    jump_count = 0  # Track number of jumps
    
    if m == 0 or n == 0 or m > n:
        print("No valid pattern or text to search.")
        return matches
    
    # Preprocess both rules
    bad_char_table = preprocess_extended_bad_character(pat)
    good_prefix_table = preprocess_good_prefix(pat)
    
    # Start with right ends aligned: pattern at position n - m
    s = n - m  # pattern starts at position s in text
    
    while s >= 0:
        j = 0  # scan from left to right
        
        # Scan pattern from left to right
        while j < m and pat[j] == txt[s + j]:
            j += 1
        
        if j == m:
            # Pattern found at position s + 1 (1-based)

            matches.append(s + 1)
            shift = good_prefix_table[0]

            s -= shift
        else:
            # Mismatch at position j
            mismatched_char = txt[s + j]
            
            # Calculate bad character shift
            bc_shift = j + 1
            if mismatched_char in bad_char_table:
                leftmost_pos = bad_char_table[mismatched_char][j]
                if leftmost_pos != -1:
                    bc_shift = leftmost_pos - j
                else:
                    bc_shift = 1
            
            # Calculate good suffix shift
            gs_shift = good_prefix_table[j] if j > 0 else 1
            
            # Use the maximum shift for optimal performance
            shift = max(gs_shift, bc_shift)

            s -= shift
        
        jump_count += 1
    

    return matches


def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python a1q2.py <text_filename> <pattern_filename>")
        sys.exit(1)
    
    # Read input files
    text_file, pattern_file = sys.argv[1], sys.argv[2]
    
    try:
        with open(text_file, 'r') as f:
            txt = f.read().strip()
        with open(pattern_file, 'r') as f:
            pat = f.read().strip()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Find pattern matches using reverse Boyer-Moore
    matches = reverse_boyer_moore(txt, pat)
    
    # Write results to output file
    with open('output_a1q2.txt', 'w') as f:
        for match_pos in matches:
            f.write(f"{match_pos}\n")
    
    print(f"Found {len(matches)} matches. Results written to output_a1q2.txt")

if __name__ == "__main__":
    main()