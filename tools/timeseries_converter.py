import xarray as xr

def read_netcdf_file(file_path):
    """
    Reads a NetCDF file using xarray and returns the dataset.

    Parameters:
    file_path (str): Path to the NetCDF file.

    Returns:
    xarray.Dataset: The dataset contained in the NetCDF file.
    """
    dataset = xr.open_dataset(file_path)
    return dataset

    def get_non_coordinate_variables(dataset):
        """
        Extracts variables that are not coordinates from the dataset.

        Parameters:
        dataset (xarray.Dataset): The dataset from which to extract variables.

        Returns:
        list: A list of variable names that are not coordinates.
        """
        non_coord_vars = [var for var in dataset.variables if var not in dataset.coords]
        return non_coord_vars

# Example usage
if __name__ == "__main__":
    file_path = 'path_to_your_netcdf_file.nc'
    dataset = read_netcdf_file(file_path)
    print(dataset)