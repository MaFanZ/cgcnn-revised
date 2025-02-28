import os
 import csv
 from itertools import permutations
 from pymatgen.core import Structure
 from pymatgen.transformations.standard_transformations
import SubstitutionTransformation
 original_folder_path = "  "
 new_folder_path = "  "
 csv_file_path = "  "
 file_list = [f for f in os.listdir(original_folder_path) if f.endswith(".cif")]  # Get the list of all files ending with ".cif" in
the folder
 os.makedirs(new_folder_path, exist_ok=True)  # Create the folder to save the new crystal structures
 structure_info = []  # Create an empty list to save the new CIF file names and their chemical formulas
 # Loop over scaling factors from 0.96 to 1.04 in intervals of 0.02
 scaling_factors = [round(x, 2) for x in list((i / 100) for i in range(96, 105, 2))]
 # Iterate over each original crystal structure file
 for scale_factor in scaling_factors:
    for file_name in file_list:
        file_path = os.path.join(original_folder_path, file_name)  # Build the full path of the original crystal structure file
        structure = Structure.from_file(file_path)  # Read the original crystal structure file
        original_formula = structure.composition.reduced_formula  # Get the chemical formula of the crystal structure
        scaled_structure = structure.copy()
        scaled_structure.scale_lattice(scale_factor)
        elements = list(set([site.species_string for site in structure.sites]))  # Get all the element types in the crystal structure
and determine the order to replace with Ag, Pd, and F
        replacements = ["Ag", "Pd", "F"]
        substitution_mapping = {elements[i]: replacements[i] for i in range(len(elements))}  # Create the substitution
mapping dictionary
        unique_permutations = list(permutations(replacements))  # Generate all unique permutations
        # Iterate over all permutations
        for i, perm in enumerate(unique_permutations, start=1):
            permutation_mapping = {elements[i]: perm[i] for i in range(len(elements))}  # Create the substitution mapping
dictionary
            substitution = SubstitutionTransformation(permutation_mapping)  # Create substitution transformation object
            new_structure = substitution.apply_transformation(structure)  # Apply substitution transformation and get the
substituted crystal structure
            new_formula = new_structure.composition.reduced_formula  # Get the chemical formula of the substituted
crystal structure
            # Build the new file path
            new_file_name = f"{new_formula}_{original_formula}_{scale_factor}_{i}.cif"
            new_file_path = os.path.join(new_folder_path, new_file_name)
            new_structure.to(filename=new_file_path)  # Write the substituted crystal structure to the new file
            structure_info.append([new_file_name, original_formula])  # Add the new CIF file name and its chemical
formula to the list
 # Save the new CIF file names and chemical formulas to a CSV file
 with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for info in structure_info:
        new_formula = info[1].replace("Ag", "Ag").replace("Pd", "Pd").replace("F", "F")  # Replace the chemical formula
elements with the "AgPdF" formula
        writer.writerow([info[0], "1"])  # Replace the second column with "1"
