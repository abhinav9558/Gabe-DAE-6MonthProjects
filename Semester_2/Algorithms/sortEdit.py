# This is the unsorted list we want to sort from lowest to highest
original_list = [7, 2, 9, 4, 1, 8, 5, 10, 3, 6]

# Define a function to sort the list without modifying the original
def sort_num():
    # Make a copy of the original list so we don’t modify it
    sorted_list = original_list[:]

    # We assume the list might need sorting, so we set swapped = True to enter the loop
    swapped = True

    # We'll keep looping until no swaps happen during a full pass
    while swapped:
        swapped = False  # Start each pass assuming no swaps will happen

        # Go through each pair of neighboring values in the list
        for i in range(len(sorted_list) - 1):
            # Compare the current number with the next one
            if sorted_list[i] > sorted_list[i + 1]:
                # If they are out of order, swap them using a temporary variable
                temp = sorted_list[i]
                sorted_list[i] = sorted_list[i + 1]
                sorted_list[i + 1] = temp

                # Since we made a swap, set swapped to True so the loop runs again
                swapped = True
    
    # Return the sorted version of the list
    return sorted_list

# Call the sort function to get a new sorted list
sorted_result = sort_num()


# Confirm original list is still unchanged
print("Original list (unchanged):", original_list)

# Print the sorted list after the function completes
print("Sorted list:", sorted_result)

