import os
import uuid
from config.global_conf import global_conf
from utils.logger import log_message

def export_dataframe_to_file(dataframe, output_format, full_data):
    """
    Export a pandas DataFrame to a file in the specified format.

    Args:
        dataframe (pd.DataFrame): The DataFrame to be exported.
        output_format (str): The format of the output file ('csv' or 'json').
        full_data (bool): Whether to export the full DataFrame or only a subset of rows.

    Returns:
        str: The path to the exported file.

    Raises:
        ValueError: If the specified output format is not supported.
        Exception: If an error occurs during the export process.
    """
    # Create export file
    output_dir = global_conf.get("DATA_FILE_EXPORT_PATH")
    file_name = f"result_{uuid.uuid4()}.{output_format}"
    file_path = os.path.join(output_dir, file_name)

    # Check
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Get data to save
        data_to_export = dataframe if full_data else dataframe.head(int(global_conf.get("MAX_ROWS_TO_LLM")))

        if output_format == "csv":
            file_content = data_to_export.to_csv(index=False)
        elif output_format == "json":
            file_content = data_to_export.to_json(orient="records", lines=False, indent=2)
        else:
            raise ValueError(f"Output file format not supported: {output_format}")

        # Write file
        with open(file_path, "w") as output_file:
            output_file.write(file_content)

        log_message("INFO", f"Successful export to file: {file_path}")

    except Exception as e:
        log_message("ERROR", f"Data export error: {str(e)}")
        raise

    return file_path