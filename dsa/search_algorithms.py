import time
import json
from xml_parser import parse_xml_to_json


def linear_search(transactions, target_id):
    """
    Linear Search Algorithm
    
    Time Complexity: O(n) where n is the number of transactions
    Space Complexity: O(1)
    
    How it works:
        1. Start at the first transaction
        2. Check if it matches the target ID
        3. If not, move to the next transaction
        4. Repeat until found or end of list reached
    
    Args:
        transactions (list): List of transaction dictionaries
        target_id (int): Transaction ID to find
        
    Returns:
        tuple: (transaction_dict or None, search_time_in_seconds)
        
    Example:
        result, time_taken = linear_search(transactions, 5)
        if result:
            print(f"Found: {result['type']}")
    """
    start_time = time.time()
    
    # Iterate through each transaction one by one
    for transaction in transactions:
        if transaction['id'] == target_id:
            end_time = time.time()
            return transaction, end_time - start_time
    
    # Not found
    end_time = time.time()
    return None, end_time - start_time


def dictionary_lookup(transaction_dict, target_id):
    """
    Dictionary (Hash Table) Lookup
    
    Time Complexity: O(1) average case, O(n) worst case
    Space Complexity: O(n) for storing the dictionary
    
    How it works:
        1. Dictionary uses a hash function to compute key location
        2. Direct access to memory location based on hash
        3. No iteration needed - instant lookup!
    
    Args:
        transaction_dict (dict): Dictionary with ID as key
        target_id (int): Transaction ID to find
        
    Returns:
        tuple: (transaction_dict or None, search_time_in_seconds)
    """
    start_time = time.time()
    
    # Direct key access - very fast!
    result = transaction_dict.get(target_id)
    
    end_time = time.time()
    return result, end_time - start_time


def create_transaction_dict(transactions):
    """
    Convert list of transactions to dictionary for fast lookups.
    
    Dictionary comprehension is used for efficiency:
        {key: value for item in list}
    
    Args:
        transactions (list): List of transaction dictionaries
        
    Returns:
        dict: Dictionary with transaction ID as key
        
    Example:
        Input list: [{'id': 1, 'amount': 100}, {'id': 2, 'amount': 200}]
        Output dict: {1: {'id': 1, 'amount': 100}, 2: {'id': 2, 'amount': 200}}
    """
    return {transaction['id']: transaction for transaction in transactions}


def binary_search(sorted_transactions, target_id):
    """
    Binary Search Algorithm (BONUS)
    
    Time Complexity: O(log n)
    Space Complexity: O(1)
    
    Requirements:
        - List must be sorted by ID
        - More efficient than linear for large datasets
    
    How it works:
        1. Check middle element
        2. If target < middle, search left half
        3. If target > middle, search right half
        4. Repeat until found or range exhausted
    
    Example with 16 elements:
        Step 1: Check position 8
        Step 2: Check position 4 or 12 (depending on comparison)
        Step 3: Check position 2, 6, 10, or 14
        Maximum 4 steps vs 16 for linear search!
    
    Args:
        sorted_transactions (list): List sorted by 'id' field
        target_id (int): Transaction ID to find
        
    Returns:
        tuple: (transaction_dict or None, search_time_in_seconds)
    """
    start_time = time.time()
    
    left = 0
    right = len(sorted_transactions) - 1
    
    while left <= right:
        # Find middle position
        mid = (left + right) // 2
        mid_transaction = sorted_transactions[mid]
        
        if mid_transaction['id'] == target_id:
            # Found it!
            end_time = time.time()
            return mid_transaction, end_time - start_time
        
        elif mid_transaction['id'] < target_id:
            # Target is in right half
            left = mid + 1
        else:
            # Target is in left half
            right = mid - 1
    
    # Not found
    end_time = time.time()
    return None, end_time - start_time


def compare_search_methods(transactions, search_ids):
    """
    Run all search methods and compare their performance.
    
    Args:
        transactions (list): List of transactions
        search_ids (list): List of IDs to search for
        
    Returns:
        dict: Results for each search method
    """
    print("\n" + "="*70)
    print("SEARCH ALGORITHM COMPARISON")
    print("="*70)
    print(f"Dataset size: {len(transactions)} transactions")
    print(f"Number of searches: {len(search_ids)}")
    print("="*70)
    
    # Prepare data structures
    trans_dict = create_transaction_dict(transactions)
    sorted_trans = sorted(transactions, key=lambda x: x['id'])
    
    results = {
        'linear': {'times': [], 'found': 0},
        'dictionary': {'times': [], 'found': 0},
        'binary': {'times': [], 'found': 0}
    }
    
    # Test each search ID
    for search_id in search_ids:
        print(f"\nSearching for ID: {search_id}")
        print("-" * 70)
        
        # Linear Search
        result_linear, time_linear = linear_search(transactions, search_id)
        results['linear']['times'].append(time_linear)
        if result_linear:
            results['linear']['found'] += 1
        print(f"  Linear Search:     {time_linear:.8f}s - {'Found' if result_linear else 'Not Found'}")
        
        # Dictionary Lookup
        result_dict, time_dict = dictionary_lookup(trans_dict, search_id)
        results['dictionary']['times'].append(time_dict)
        if result_dict:
            results['dictionary']['found'] += 1
        print(f"  Dictionary Lookup: {time_dict:.8f}s - {'Found' if result_dict else 'Not Found'}")
        
        # Binary Search
        result_binary, time_binary = binary_search(sorted_trans, search_id)
        results['binary']['times'].append(time_binary)
        if result_binary:
            results['binary']['found'] += 1
        print(f"  Binary Search:     {time_binary:.8f}s - {'Found' if result_binary else 'Not Found'}")
    
    # Calculate averages
    print("\n" + "="*70)
    print("PERFORMANCE SUMMARY")
    print("="*70)
    
    for method, data in results.items():
        avg_time = sum(data['times']) / len(data['times']) if data['times'] else 0
        print(f"\n{method.upper()} SEARCH:")
        print(f"  Average time:  {avg_time:.8f}s")
        print(f"  Total time:    {sum(data['times']):.8f}s")
        print(f"  Found:         {data['found']}/{len(search_ids)}")
    
    # Calculate speedup
    linear_avg = sum(results['linear']['times']) / len(results['linear']['times'])
    dict_avg = sum(results['dictionary']['times']) / len(results['dictionary']['times'])
    binary_avg = sum(results['binary']['times']) / len(results['binary']['times'])
    
    print("\n" + "="*70)
    print("SPEEDUP ANALYSIS")
    print("="*70)
    if dict_avg > 0:
        print(f"Dictionary is {linear_avg / dict_avg:.2f}x faster than Linear Search")
    if binary_avg > 0:
        print(f"Binary Search is {linear_avg / binary_avg:.2f}x faster than Linear Search")
        print(f"Dictionary is {binary_avg / dict_avg:.2f}x faster than Binary Search")
    print("="*70 + "\n")
    
    return results


def analyze_complexity():
    """
    Print theoretical complexity analysis.
    """
    print("\n" + "="*70)
    print("THEORETICAL TIME COMPLEXITY ANALYSIS")
    print("="*70)
    
    print("\n1. LINEAR SEARCH:")
    print("   Time Complexity: O(n)")
    print("   Space Complexity: O(1)")
    print("   - Best case: O(1) - element is first")
    print("   - Average case: O(n/2) = O(n)")
    print("   - Worst case: O(n) - element is last or not present")
    print("   - Must check every element in worst case")
    
    print("\n2. DICTIONARY LOOKUP:")
    print("   Time Complexity: O(1) average")
    print("   Space Complexity: O(n)")
    print("   - Best case: O(1)")
    print("   - Average case: O(1)")
    print("   - Worst case: O(n) - hash collisions")
    print("   - Uses hash table for instant access")
    print("   - Trade-off: Uses extra memory")
    
    print("\n3. BINARY SEARCH:")
    print("   Time Complexity: O(log n)")
    print("   Space Complexity: O(1)")
    print("   - Requires sorted data")
    print("   - Best case: O(1) - element is middle")
    print("   - Average case: O(log n)")
    print("   - Worst case: O(log n)")
    print("   - Divides search space in half each step")
    
    print("\n" + "="*70)
    print("WHY IS DICTIONARY FASTER?")
    print("="*70)
    print("""
1. HASH FUNCTION: Python dictionaries use a hash function that converts
   the key (transaction ID) into a memory address. This is nearly instant.

2. DIRECT ACCESS: Instead of checking each item one by one, the hash
   function tells us exactly where to look in memory.

3. CONSTANT TIME: Whether you have 10 or 10,000 transactions, lookup
   time remains roughly the same.

4. THE TRADE-OFF: Dictionaries use more memory because they maintain
   a hash table structure. This is a classic space-time trade-off.

EXAMPLE:
   Finding ID=500 in 1000 transactions:
   - Linear Search: Must check ~500 items on average
   - Dictionary: Hash 500 → Jump to location → Get value (1 operation!)
    """)
    print("="*70 + "\n")


def suggest_alternatives():
    """
    Suggest other data structures and algorithms.
    """
    print("\n" + "="*70)
    print("ALTERNATIVE DATA STRUCTURES & ALGORITHMS")
    print("="*70)
    
    print("\n1. BINARY SEARCH TREE (BST):")
    print("   - Time: O(log n) average for balanced tree")
    print("   - Keeps data sorted automatically")
    print("   - Good for range queries (find all IDs between 10-20)")
    
    print("\n2. HASH TABLE WITH CHAINING:")
    print("   - Better collision handling than basic dictionary")
    print("   - Maintains O(1) even with many collisions")
    
    print("\n3. B-TREE:")
    print("   - Used in databases")
    print("   - Excellent for disk-based storage")
    print("   - O(log n) but fewer disk reads")
    
    print("\n4. TRIE (for string searches):")
    print("   - If searching by transaction_id as string")
    print("   - Fast prefix matching")
    
    print("\n5. BLOOM FILTER:")
    print("   - Space-efficient for existence checking")
    print("   - Can quickly say 'definitely not present'")
    print("   - Small false positive rate")
    
    print("\n6. INDEXED DATABASE:")
    print("   - For very large datasets")
    print("   - Multiple indexes on different fields")
    print("   - SQL: CREATE INDEX ON transactions(id)")
    
    print("="*70 + "\n")


# Example usage and testing
if __name__ == '__main__':
    import sys
    import os
    
    # Get XML file path
    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
    else:
        xml_file = '../modified_sms_v2.xml'
    
    print(f"Loading transactions from: {xml_file}\n")
    
    # Parse transactions
    transactions = parse_xml_to_json(xml_file)
    
    if not transactions:
        print("No transactions loaded. Please check the XML file path.")
        sys.exit(1)
    
    # Select test IDs (first 20, plus some random ones)
    test_ids = list(range(1, min(21, len(transactions) + 1)))
    
    # Add some IDs from middle and end
    if len(transactions) > 100:
        test_ids.extend([
            len(transactions) // 2,  # Middle
            len(transactions) - 10,  # Near end
            len(transactions)        # Last
        ])
    
    # Add a non-existent ID to test not found case
    test_ids.append(99999)
    
    print(f"Testing with {len(test_ids)} search queries...")
    
    # Run comparison
    results = compare_search_methods(transactions, test_ids)
    
    # Print theoretical analysis
    analyze_complexity()
    
    # Suggest alternatives
    suggest_alternatives()
    
    # Save results to JSON
    output = {
        'dataset_size': len(transactions),
        'searches_performed': len(test_ids),
        'results': results
    }
    
    with open('search_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print("Results saved to search_results.json")
