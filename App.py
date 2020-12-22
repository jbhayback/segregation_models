import numpy as np
import pandas as pd
import streamlit as st
import sys

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from Schelling import Schelling as SchellingModel
from Dissimilarity import Dissimilarity as DissimilaritySegregationModel

def count_char(tract_data, char_to_count):
    # Counts specific char from each tract of char sequence obtained via get_splitted_data function
    char_count = 0
    for sub_array in tract_data:
        char_count += np.count_nonzero(sub_array == char_to_count)
    
    return char_count

def validate_data_for_invalid_chars(raw_input_data):
    # Validates the input data if there are invalid characters.
    total_population = int(raw_input_data.shape[0] * raw_input_data.shape[1])

    # Only X, O and empty/null characters sequence are allowed
    X_char_count = count_char(raw_input_data.values, 'X')
    O_char_count = count_char(raw_input_data.values, 'O')
    empty_char_count = count_char(raw_input_data.values, '')

    # Returns false if there are characters other than accepted character sequence
    return total_population == (X_char_count + O_char_count + empty_char_count)

def validate_row_column_inputs(raw_input_data, input_row, input_column):
    # Validates the input row and colums can successfully split the Data Grid into possible tracts for Index of Dissimilarity calculation
    total_population = int(raw_input_data.shape[0] * raw_input_data.shape[1])

    # Returns True if the row and column inputs are multiples of total population for getting population of each tract
    # Each tract should have the same population
    if (total_population % (input_row * input_column) != 0):
        return [False, "NOT_MULTIPLE"]
    elif raw_input_data.shape[0] % input_row != 0 or raw_input_data.shape[1] % input_column != 0:
        return [False, "CANT_SPLIT"]

    return [True, "SUCCESS"]

def convert_char_seq_to_numeric_grid(raw_input_data):
    # Converts char sequence to numeric equivalent prior to processing. X is 1, O is -1 and empty/null to O
    # Raw input data should be cleaned and converted to numeric value prior processing
    converted_input_data = raw_input_data.replace('', 0).replace('X', 1).replace('O', -1)

    return converted_input_data

def convert_numeric_grid_to_char_seq_grid(numeric_grid):
    # Converts numeric sequence to char equivalent as the final output for display. 1 is X, -1 is O and 0 to empty/null
    raw_input_dataframe = pd.DataFrame(numeric_grid)
    converted_output_data = raw_input_dataframe.replace(0, '').replace(1, 'X').replace(-1, 'O')

    return converted_output_data

def main():
    st.sidebar.subheader("Input Data")
    input_file_path = st.sidebar.text_input('CSV file path' , 'Input_data.csv')
    st.sidebar.subheader("")

    try:
        # Gets the raw input data from the input csv file path from user
        raw_input_data = pd.read_csv(input_file_path).fillna('')
    except:
        # When the path of the csv file is invalid, system exits and throws an error message
        sys.exit('Invalid path or csv file! Please input valid path or csv file.')

    if (validate_data_for_invalid_chars(raw_input_data)):
        converted_input_data = convert_char_seq_to_numeric_grid(raw_input_data)
        population_size = int(converted_input_data.shape[0] * converted_input_data.shape[1])

        # Streamlit Apps
        #####################################
        # Dissimilarity (Segregation Model) #
        #####################################
        st.title("Dissimilarity : Segregation Model")
        st.sidebar.subheader("Dissimilarity : Segregation Model Inputs")
        input_row = st.sidebar.number_input("Number of Rows per Tract", 1)
        input_col = st.sidebar.number_input("Number of Columns per Tract", 1)
        st.header('Original Data Grid')
        st.dataframe(raw_input_data.values);

        if st.sidebar.button('Calculate Index of Dissimilarity'):
            is_valid_row_col_input = validate_row_column_inputs(raw_input_data, input_row, input_col)
            if is_valid_row_col_input[0]:
                dissimilarity = DissimilaritySegregationModel(raw_input_data)
                total_number_of_tracts = int(population_size/(input_row*input_col))
                partial_indices = []

                data_tracts = dissimilarity.get_splitted_data(input_row, input_col)
                print(type(data_tracts))
                tract_number = 1
                for data_per_tract in data_tracts:
                    partial_index = dissimilarity.calculate_partial_index(data_per_tract)
                    partial_indices.append(partial_index)

                    st.text('Data Grid for Tract ' + str(tract_number) + ' with Partial Index: ' + str(round(partial_index, 2)))
                    st.dataframe(data_per_tract)
                    tract_number += 1

                D = round(0.5*sum(partial_indices), 2)
                st.sidebar.subheader("Index of Dissimilarity: " + str(D))

            else:
                if is_valid_row_col_input[1] == "NOT_MULTIPLE":
                    st.error("The population per tract (No. of Row x No. of Column) is: " + str(input_row*input_col) + ". It should be a multiple of the total population: " + str(population_size))
                else:
                    st.error("Cannot split the data grid with equal number of characterss per tract/splice based on the input row or column.")
                st.error("Please enter valid data.")

        ##################################
        # Schelling's Segregartion Model #
        ##################################
        st.title("Schelling's Segregation Model")
        st.sidebar.subheader("")
        st.sidebar.subheader("Schelling's Segregation Model Inputs")
        similarity_threshold = st.sidebar.slider("Similarity Threshold", 0., 1., .4)
        n_iterations = st.sidebar.number_input("Number of Iterations", 20)

        schelling = SchellingModel(converted_input_data, similarity_threshold, 3)
        mean_similarity_ratio = []
        mean_similarity_ratio.append(schelling.get_average_similarity_ratio())

        # Plot the graphs at initial stage
        plt.style.use("ggplot")
        plt.figure(figsize=(8, 4))

        # Left hand side graph with Schelling simulation plot
        cmap = ListedColormap(['royalblue', 'white', 'red'])
        plt.subplot(121)
        plt.axis('off')
        plt.title("X - Red \nO - Blue", fontsize=10)
        plt.pcolor(schelling.data_grid, cmap=cmap, edgecolors='w', linewidths=1)
        plt.gca().invert_yaxis()

        # Right hand side graph with Mean Similarity Ratio graph
        plt.subplot(122)
        plt.xlabel("Iterations")
        plt.xlim([0, n_iterations])
        plt.ylim([0.4, 1])
        plt.title("Mean Similarity Ratio", fontsize=12)
        plt.text(1, 0.95, "Similarity Ratio: %.4f" % schelling.get_average_similarity_ratio(), fontsize=10)

        data_grid_plot = st.pyplot(plt)
        progress_bar = st.progress(0)

        new_satisfied_data_grid = np.array([])
        if st.sidebar.button('Run Schelling Simulation'):
            current_largest_mean_sim_ratio = schelling.get_average_similarity_ratio();
            for i in range(n_iterations):
                # Starts running the Schelling Model Simulation
                schelling.run_simulation()
                latest_sim_ratio = schelling.get_average_similarity_ratio()
                if current_largest_mean_sim_ratio < latest_sim_ratio:
                    current_largest_mean_sim_ratio = latest_sim_ratio
                    new_satisfied_data_grid = schelling.data_grid
                mean_similarity_ratio.append(schelling.get_average_similarity_ratio())
                plt.figure(figsize=(8, 4))
            
                # Plotting the current Data Grid
                plt.subplot(121)
                plt.axis('off')
                plt.title("X - Red \nO - Blue", fontsize=10)
                plt.pcolor(schelling.data_grid, cmap=cmap, edgecolors='w', linewidths=1)
                plt.gca().invert_yaxis()

                plt.subplot(122)
                plt.xlabel("Iterations")
                plt.xlim([0, n_iterations])
                plt.ylim([0.4, 1])
                plt.title("Mean Similarity Ratio", fontsize=15)
                plt.plot(range(1, len(mean_similarity_ratio)+1), mean_similarity_ratio)
                plt.text(1, 0.95, "Similarity Ratio: %.4f" % schelling.get_average_similarity_ratio(), fontsize=10)

                data_grid_plot.pyplot(plt)
                plt.close("all")
                progress_bar.progress((i+1.)/n_iterations)

        if new_satisfied_data_grid.size != 0:
            # Display the new data grid with satisfied neighboring characters
            new_data_grid_df = convert_numeric_grid_to_char_seq_grid(new_satisfied_data_grid)
            st.header("New Data Grid with Satisfied Neighboring Characters")
            st.dataframe(new_data_grid_df)

            # Save output to Output.csv file
            pd.DataFrame(new_data_grid_df).to_csv('Output_data.csv', index=False)

    else:
        st.error('ERROR: Invalid characters in the data. Please check dataset from Input_data.csv and retry.')

if __name__ == "__main__":
    main()
