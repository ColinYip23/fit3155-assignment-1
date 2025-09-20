"""
BWT-based pattern matching with wildcard support
Pattern may contain '#' characters that match any character in text
"""

import sys

def construct_bwt_naive(txt):
    """
    Construct BWT using naive method (sorting cyclic permutations)
    Returns: BWT string and suffix array
    """
    n = len(txt)
    if n == 0:
        return "", []
    
    # Create all cyclic rotations
    rotations = []
    for i in range(n):
        rotation = txt[i:] + txt[:i]
        rotations.append((rotation, i))
    
    # Sort rotations lexicographically
    rotations.sort(key=lambda x: x[0])
    
    # Extract BWT (last characters of sorted rotations) and suffix array
    bwt = ''.join(rotation[0][-1] for rotation in rotations)
    suffix_array = [rotation[1] for rotation in rotations]
    
    return bwt, suffix_array

def create_rank_arrays(bwt):
    """
    Create rank arrays for BWT to enable efficient LF mapping
    Returns: rank arrays and first occurrence mapping
    """
    n = len(bwt)
    chars = sorted(set(bwt))
    
    # Create rank arrays for each character
    rank_arrays = {}
    for c in chars:
        rank_arrays[c] = [0] * (n + 1)
    
    # Create cumulative counts
    for i in range(n):
        for c in chars:
            rank_arrays[c][i + 1] = rank_arrays[c][i] + (1 if bwt[i] == c else 0)
    
    # Create first occurrence mapping
    first_occurrence = {}
    cumulative = 0
    for c in chars:
        first_occurrence[c] = cumulative
        cumulative += rank_arrays[c][n]
    
    return rank_arrays, first_occurrence

def backward_search_with_wildcards(bwt, first_occurrence, rank_arrays, pat, suffix_array):
    """
    Perform backward search on BWT for pattern with wildcards
    Returns: list of matching positions
    """
    n = len(bwt)
    m = len(pat)
    matches = set()
    
    if m == 0:
        return []
    
    # Start with the entire BWT range
    ranges = [(0, n - 1, m - 1)]  # (start, end, pattern_index)
    
    while ranges:
        start, end, idx = ranges.pop()
        
        # If we've processed the entire pattern, add all matches in this range
        if idx < 0:
            for i in range(start, end + 1):
                matches.add(suffix_array[i])
            continue
        
        c = pat[idx]
        
        if c == '#':
            # Wildcard: try all possible characters
            for char in rank_arrays.keys():
                if char == '$':  # Skip terminator if present
                    continue
                
                # Calculate new range for this character
                new_start = first_occurrence.get(char, 0) + rank_arrays[char][start]
                new_end = first_occurrence.get(char, 0) + rank_arrays[char][end + 1] - 1
                
                if new_start <= new_end:
                    ranges.append((new_start, new_end, idx - 1))
        else:
            # Regular character
            if c not in rank_arrays:
                continue  # Character not in text
            
            # Calculate new range using LF mapping
            new_start = first_occurrence[c] + rank_arrays[c][start]
            new_end = first_occurrence[c] + rank_arrays[c][end + 1] - 1
            
            if new_start <= new_end:
                ranges.append((new_start, new_end, idx - 1))
    
    return sorted(matches)

def find_pattern_matches_bwt(txt, pat):
    """
    Find all occurrences of pattern in text using BWT
    Pattern may contain '#' wildcards that match any character
    """
    n, m = len(txt), len(pat)
    
    # Handle edge cases
    if m == 0 or n == 0 or m > n:
        return []
    
    # Add terminator character (assuming '$' doesn't appear in text)
    txt_with_terminator = txt + '$'
    
    # Construct BWT and suffix array
    bwt, suffix_array = construct_bwt_naive(txt_with_terminator)
    
    # Create rank arrays and first occurrence mapping
    rank_arrays, first_occurrence = create_rank_arrays(bwt)
    
    # Perform backward search with wildcards
    matches = backward_search_with_wildcards(bwt, first_occurrence, rank_arrays, pat, suffix_array)
    
    # Filter out matches that would extend beyond text (due to terminator)
    valid_matches = [pos for pos in matches if pos + m <= n]
    
    return valid_matches

def main():
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python a1q3.py <text_filename> <pattern_filename>")
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
    
    # Find pattern matches using BWT
    matches = find_pattern_matches_bwt(txt, pat)
    
    # Write results to output file (1-based indexing)
    with open('output_a1q3.txt', 'w') as f:
        for match_pos in matches:
            # Convert to 1-based indexing as specified
            f.write(f"{match_pos + 1}\n")
    
    print(f"Found {len(matches)} matches. Results written to output_a1q3.txt")

if __name__ == "__main__":
    main()