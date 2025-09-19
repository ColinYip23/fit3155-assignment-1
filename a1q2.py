"""
Reverse Boyer-Moore algorithm implementation
Pattern shifts leftwards along the text, scanning from left to right
"""

import sys

def preprocess_bad_character_right(pat):
    """
    Preprocess bad character shift table for right-to-left scanning
    Returns: dictionary of bad character shifts
    Key insight: For left-to-right scanning, we need the leftmost occurrence
    of each character from the RIGHT side of the current position
    """
    m = len(pat)
    bad_char = {}
    
    # For each character, store the rightmost occurrence position
    # This helps us determine how far to shift when we find a mismatch
    for i in range(m):
        # Store the position where this character last appears
        bad_char[pat[i]] = i
    
    return bad_char

def calculate_shift(bad_char, mismatched_char, current_pos):
    """
    Calculate shift distance based on bad character rule
    current_pos: position in pattern where mismatch occurred
    """
    if mismatched_char in bad_char:
        # Character exists in pattern
        pattern_pos = bad_char[mismatched_char]
        if pattern_pos < current_pos:
            # Shift to align the pattern occurrence with text position
            return current_pos - pattern_pos
        else:
            # Character occurs at or after current position, shift by 1
            return 1
    else:
        # Character not in pattern, shift past it
        return current_pos + 1

def reverse_boyer_moore(txt, pat):
    """
    Reverse Boyer-Moore algorithm that shifts pattern leftwards
    and scans from left to right
    """
    n, m = len(txt), len(pat)
    matches = []
    
    if m == 0 or n == 0 or m > n:
        return matches
    
    # Preprocess bad character table
    bad_char = preprocess_bad_character_right(pat)
    
    # Start with right ends aligned: pattern at position n - m
    s = n - m  # Current shift (pattern starts at position s in text)
    
    while s >= 0:
        j = 0  # Pattern index (scan from left to right)
        
        # Scan pattern from left to right
        while j < m and pat[j] == txt[s + j]:
            j += 1
        
        if j == m:
            # Pattern found at position s + 1 (1-based)
            matches.append(s + 1)
            # Shift left by 1 for next potential match
            s -= 1
        else:
            # Mismatch at position j in pattern
            mismatched_char = txt[s + j]
            shift = calculate_shift(bad_char, mismatched_char, j)
            s -= shift  # Shift pattern leftwards
    
    return matches

def test_example():
    """Test with the provided example"""
    txt = "aabbabababbbbaabaabbabbaa"
    pat = "aba"
    
    print(f"Text: {txt}")
    print(f"Pattern: {pat}")
    
    matches = reverse_boyer_moore(txt, pat)
    print(f"Matches found: {matches}")
    print("Expected: [15, 7, 5]")

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
    # test_example()  # Uncomment to test with the example
    main()