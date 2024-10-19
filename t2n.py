"""
Created on Oct 2024
@author: Agamdeep Chopra
@email: achopra4@uw.edu
@website: https://agamchopra.github.io/
"""
import os
import glob
import numpy as np
from PIL import Image
from scipy.ndimage import zoom
import nibabel as nib
import argparse


def project_average_along_z(array):
    # Project the average along the z-axis
    average_projection = np.mean(array, axis=-1)

    return average_projection


def save_array_as_nii(array, file_path):
    # Create a Nifti1Image from the numpy array
    nii_image = nib.Nifti1Image(array, affine=np.eye(4))

    # Save the Nifti image to the specified file path
    nib.save(nii_image, file_path)


def calculate_max_dim_length(arr1, arr2, arr3):
    # Calculate the maximum length for each dimension
    max_dim_lengths = [max(arr1.shape[i], arr2.shape[i],
                           arr3.shape[i]) for i in range(3)]

    return max_dim_lengths


def resample_3d_array(array_3d, target_shape):
    # Calculate the zoom factors for each dimension
    zoom_factors = [t / s for t, s in zip(target_shape, array_3d.shape)]

    # Perform nearest neighbor interpolation using zoom
    resampled_array = zoom(array_3d, zoom_factors, order=0)

    return resampled_array


def load_stack_to_3d_matrix(folder_path):
    # Get sorted list of file paths based on index number
    file_pattern = f"{folder_path}*.tif"
    file_paths = sorted(glob.glob(file_pattern))

    if not file_paths:
        raise FileNotFoundError(
            "No .tif files found in the specified folder with the given prefix.")

    # Load the first image to get dimensions
    with Image.open(file_paths[0]) as img:
        width, height = img.size
        first_image_array = np.array(img)

    # Initialize an empty 3D NumPy array
    num_images = len(file_paths)
    stack_3d = np.zeros((num_images, height, width),
                        dtype=first_image_array.dtype)

    # Load all images into the 3D matrix
    for idx, file_path in enumerate(file_paths):
        with Image.open(file_path) as img:
            stack_3d[idx] = np.array(img)

    return stack_3d


def load_rgb_stack(folder_path, sample_id):
    folder_path_r = os.path.join(folder_path, f'{sample_id}_w435_z')
    folder_path_g = os.path.join(folder_path, f'{sample_id}_w523_z')
    folder_path_b = os.path.join(folder_path, f'{sample_id}_w594_z')

    stack_b = load_stack_to_3d_matrix(folder_path_r)
    stack_g = load_stack_to_3d_matrix(folder_path_g)
    stack_r = load_stack_to_3d_matrix(folder_path_b)

    max_dims = calculate_max_dim_length(stack_r, stack_g, stack_b)

    stack_rgb = np.array([resample_3d_array(stack, max_dims)
                         for stack in (stack_r, stack_g, stack_b)])

    stack_rgb = np.transpose(stack_rgb, (0, 2, 3, 1))

    return stack_rgb


def tifz2nifiti(target_folder, output_folder, sample_id, mode='3D'):
    try:
        stack = load_rgb_stack(target_folder, sample_id)
        print(f'Stack created: {stack.shape}')
    except Exception:
        print(f'ERROR: Unable to create 3D rgb stack! Make sure that that the target folder is correct {
              target_folder}. Please check the .tif z-stacks are correct and the sample ID is correct {sample_id}')
    if mode == 'proj':
        try:
            print('Projection mode selected...')
            stack = project_average_along_z(stack)
            output_file = os.path.join(
                output_folder, f'{sample_id}_PROJ.nii.gz')
            print(f'Stack projected(average alond Z-dim) to 2D: {stack.shape}')
        except Exception:
            output_file = os.path.join(output_folder, f'{sample_id}.nii.gz')
            print('Unable to project to 2D, attempting to save as 3D instead...')
    else:
        print('3D mode selected, please use mode=\'proj\' to save as 2D projection...')
        output_file = os.path.join(output_folder, f'{sample_id}.nii.gz')
    try:
        save_array_as_nii(stack, output_file)
        print(f'Image saved at {output_file}')
    except Exception:
        print(f'ERROR: Unable to save image at {output_file}')


def main():
    parser = argparse.ArgumentParser(
        description="Convert .tif z-stacks to NIfTI format.")
    parser.add_argument("target_folder", type=str,
                        help="Path to the folder containing input .tif files.")
    parser.add_argument("output_folder", type=str,
                        help="Path to the folder where the output .nii.gz file will be saved.")
    parser.add_argument("sample_id", type=str,
                        help="Sample ID used to find the specific .tif z-stacks.")
    parser.add_argument("--mode", type=str, choices=["3D", "proj"], default="3D",
                        help="Mode for saving output: '3D' for 3D stack or 'proj' for 2D projection.")

    args = parser.parse_args()

    tifz2nifiti(args.target_folder, args.output_folder,
                args.sample_id, mode=args.mode)


if __name__ == "__main__":
    main()
