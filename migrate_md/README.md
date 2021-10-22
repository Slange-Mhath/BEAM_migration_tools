# Pre-Ingest-Metadata-Migration Tool

This script allows users to convert their xsl files into json, use the name of
the columns as keys and relabel them to different keys if needed. 
This script is mainly developed in context of the BEAM project, and thus 
specified to its needs, but basic functionality can also be used for 
any other form of conversion from Excel files to json and simultaneous 
renaming of their column names.

# How to use

The easiest way to execute the script is to run it through the terminal providing
the arguments of which are 2 mandatory:

1. `"acc_folder_path"` specifies the folder where the xls files are located. The 
exact folder structure isn't important, which means that files in subfolders are
also respected.
   
2. `"output_file_prefix"` specifies a path/name of the relabeled and migrated 
   outputfile which will be in json and ending with the accession name.
   The format of the filename will be something like 
   output_file_myaccession.json
   
As an optional argument the user can specify a `"list_of_keys"` while this 
argument should point to a json file which contains a list of keys as dicts (for
example the one created by the [Read metadata model tool](
https://github.com/Slange-Mhath/BEAM_migration_tools/tree/main/read_md_model)).
If this argument isn't provided then the script will take the hardcoded list of
keys which was specified by the BEAM archivists. 


`$ cd /migrate_md`

`$ python3 main.py "my_accession_folder" "output_file_prefix"`

or if you want to specify another list_of_keys:

`$ python3 main.py "my_accession_folder" "output_file_prefix" --list_of_keys "path_to_key_list.json"`



# Dependencies

Please use Python 3.x

This script relies on:
- [panda](
https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
  
- [json](https://docs.python.org/3/library/json.html)

- [os](https://docs.python.org/3/library/os.html)

- [argparse](https://docs.python.org/3/library/argparse.html)

- [sys](https://docs.python.org/3/library/sys.html)

- [logging](https://docs.python.org/3/howto/logging.html)



