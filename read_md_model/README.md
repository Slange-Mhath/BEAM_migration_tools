# Read Metadata model file tool

This script allows users to read the specified metadata model file as xsl and
extract all the keys needed for the relabeling and migration. (e.g. for the 
[Pre-Ingest-Migration Tool](https://github.com/Slange-Mhath/BEAM_migration_tools/tree/main/migrate_md))
This list of keys can be written to the terminal or to a specified json file.



# How to use

The easiest way to execute the script is to run it through the terminal providing
the arguments of which are 4 mandatory:

1. `"md_model"` specifies the full path to the xls file which has the 
   metadata_model specifications.
   
2. `"sheet_name"` specifies the name of the worksheet in the xls file.

3. `"col_old_label"` specifies the column in the xls file where the old labels are
specified
   
4. `"col_new_label"` the column in the xls file where the new labels are
specified (These will replace the ones in the column of old labels).
   
   
As an optional argument the user can specify an `"--output"`. This will create a
file where the list with the keys is stored. Recommended is a json file as 
argunment.

For example `--output "my_key_list.json"`

## Steps to run the script: 

`$ cd /read_md_model`

`$ python3 main.py "my_metadata_model.xlsx" "Pre-ingest" "Label as exists in legacy metadata (BEAM spreadsheet, metadata field)" "New local label" --output "my_key_list.json"`




# Dependencies

Please use Python 3.x

This script relies on:
- [pandas](
https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
  
- [json](https://docs.python.org/3/library/json.html)

- [os](https://docs.python.org/3/library/os.html)

- [argparse](https://docs.python.org/3/library/argparse.html)

- [sys](https://docs.python.org/3/library/sys.html)

- [logging](https://docs.python.org/3/howto/logging.html)



