"""
Z-algorithm based pattern matching with wildcard support
Pattern may contain '#' characters that match any character in text
"""

import sys

def compute_z_array(s):
    """
    Compute Z-array for string s using the Z-algorithm
    Z[i] = length of longest substring starting at i that matches prefix of s
    """
    n = len(s)
    z = [0] * n
    l, r = 0, 0  # left and right boundaries of current Z-box
    
    for i in range(1, n):
        if i > r:
            # Case 1: i is outside current Z-box
            l, r = i, i
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            # Case 2: i is inside current Z-box
            k = i - l
            if z[k] < r - i + 1:
                # Case 2a: Z[k] < remaining length in Z-box
                z[i] = z[k]
            else:
                # Case 2b: Z[k] >= remaining length, need to extend
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    return z

def find_pattern_matches(txt, pat):
    """
    Find all occurrences of pattern in text using Z-algorithm
    Pattern may contain '#' wildcards that match any character
    """
    n, m = len(txt), len(pat)
    matches = []
    
    if m == 0 or m > n:
        return matches
    
    # Create combined string: pattern + '$' + text
    # We use '$' as a separator that doesn't appear in text or pattern
    combined = pat + '$' + txt
    
    # Compute Z-array for the combined string
    z_array = compute_z_array(combined)
    
    # Check for matches starting at each position in text
    # The text part starts at index m+1 in the combined string
    for i in range(m + 1, len(combined) - m + 1):  # Ensure we don't go out of bounds
        # The Z-value at position i in combined string
        # indicates the length of match with pattern prefix
        if z_array[i] == m:
            # Exact match found (position in text = i - m - 1)
            matches.append(i - m - 1)
        elif z_array[i] < m:
            # Partial match, check if we can complete the match with wildcards
            matched_length = z_array[i]
            
            # Check if we have enough characters remaining in text
            text_pos = i - m - 1  # Actual position in original text
            if text_pos + m > n:  # Pattern would extend beyond text
                continue
                
            # Check if the remaining pattern characters are all wildcards
            # or match the corresponding text characters
            valid_match = True
            for j in range(matched_length, m):
                # Calculate position in combined string
                combined_pos = i + j
                if combined_pos >= len(combined):
                    valid_match = False
                    break
                
                if pat[j] == '#':
                    # Wildcard matches any character
                    continue
                elif pat[j] != combined[combined_pos]:
                    # Character doesn't match and it's not a wildcard
                    valid_match = False
                    break
            
            if valid_match:
                matches.append(text_pos)
    
    return matches

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python a1q1.py <text_filename> <pattern_filename>")
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
    
    # Find pattern matches
    matches = find_pattern_matches(txt, pat)
    
    # Write results to output file (1-based indexing)
    with open('output_a1q1.txt', 'w') as f:
        for match_pos in matches:
            # Convert to 1-based indexing as specified
            f.write(f"{match_pos + 1}\n")
    
    print(f"Found {len(matches)} matches. Results written to output_a1q1.txt")

if __name__ == "__main__":
    main()