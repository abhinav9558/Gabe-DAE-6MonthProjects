# This is the unsorted list we want to sort from lowest to highest
original_list = [7, 2, 9, 4, 1, 8, 5, 10, 3, 6]

# Print the original list before sorting
print("Original list:", original_list)

# Define a function to sort the list
def sort_num():

    # We assume the list might need sorting, so we set swapped = True to enter the loop
    swapped = True

    # We'll keep looping until no swaps happen during a full pass
    while swapped:
        swapped = False  # Start each pass assuming no swaps will happen

        # Go through each pair of neighboring values in the list
        for i in range(len(original_list) - 1):
            # Compare the current number with the next one
            if original_list[i] > original_list[i + 1]:
                # If they are out of order, swap them using a temporary variable
                temp = original_list[i]
                original_list[i] = original_list[i + 1]
                original_list[i + 1] = temp

                # Since we made a swap, set swapped to True so the loop runs again
                swapped = True

# Call the sort function to sort the list
sort_num()

# Print the sorted list after the function completes
print("Sorted list:", original_list)