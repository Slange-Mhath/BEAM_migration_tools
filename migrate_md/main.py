import os
import json
import pandas as pd
import logging
import sys
from argparse import ArgumentParser

if sys.version_info[0] == 2:
    raise Exception("Please use Python 3")


base_path = "set_of_accnotes"

LIST_OF_KEYS = [{'new_label': 'collection_id',
  'old_label': 'collection name',
  'old_labels': 'datadiskinventory, collection name; transferinventory, '
                'collection name; audiodiskinventory, collection name; '
                'videodiskinventory, collection name '},
 {'new_label': 'beam_container_id',
  'old_label': 'beam container id',
  'old_labels': 'datadiskinventory, BEAM container ID; transferinventory, BEAM '
                'container ID; audiodiskinventory, BEAM container ID; '
                'videodiskinventory, BEAM container ID'},
 {'new_label': 'accession_id',
  'old_label': 'accession id',
  'old_labels': 'datadiskinventory, accession id; transferinventory, accession '
                'id; audiodiskinventory, accession id; videodiskinventory, '
                'accession id'},
 {'new_label': 'date_metadata_created',
  'old_label': 'date record created',
  'old_labels': 'datadiskinventory, date record created; transferinventory, '
                'date record created; audiodiskinventory, date record created; '
                'videodiskinventory, date record created'},
 {'new_label': 'date_metadata_modified',
  'old_label': 'date record modified',
  'old_labels': 'datadiskinventory, date record modified; transferinventory, '
                'date record modified; audiodiskinventory, date record '
                'modified; videodiskinventory, date record modified'},
 {'new_label': 'legacy_container_id',
  'old_label': 'legacy container id',
  'old_labels': 'datadiskinventory, legacy container id; transferinventory, '
                'legacy container id; videodiskinventory, legacy container id; '
                'audiodiskinventory, legacy container id'},
 {'new_label': 'metadata_create_agent',
  'old_label': 'name of person who created the record',
  'old_labels': 'datadiskinventory, name of person who created the record; '
                'transferinventory, name of person who created the record; '
                'videodiskinventory, name of person who created the record; '
                'audiodiskinventory, name of person who created the record'},
 {'new_label': 'metatadata_modified_agent',
  'old_label': 'name of person who modified the record',
  'old_labels': 'datadiskinventory, name of person who modified the record; '
                'transferinventory, name of person who modified the record; '
                'videodiskinventory, name of person who modified the record; '
                'audiodiskinventory, name of person who modified the record'},
 {'new_label': 'media_photos',
  'old_label': 'associated photos',
  'old_labels': 'datadiskinventory, associated photos; transferinventory, '
                'associated photos; audiodiskinventory, associated photos; '
                'videodiskinventory, associated photos'},
 {'new_label': 'media_brand',
  'old_label': 'brand',
  'old_labels': 'datadiskinventory, brand; audiodiskinventory, brand; '
                'videodiskinventory, brand'},
 {'new_label': 'media_capacity_bytes',
  'old_label': 'capacity [bytes]',
  'old_labels': 'datadiskinventory, capacity [bytes]; audiodiskinventory, '
                'capacity [bytes]; videodiskinventory, capacity [bytes]'},
 {'new_label': 'media_capacity_used',
  'old_label': 'capacity [used]',
  'old_labels': 'datadiskinventory, capacity [used]; audiodiskinventory, '
                'capacity [used]; videodiskinventory, capacity [used]'},
 {'new_label': 'media_comments',
  'old_label': 'comments',
  'old_labels': 'datadiskinventory, comments; audiodiskinventory, comments; '
                'videodiskinventory, comments'},
 {'new_label': 'transfer_comments',
  'old_label': 'comments;',
  'old_labels': 'transferinventory, comments; '},
 {'new_label': 'file_sytem',
  'old_label': 'file system',
  'old_labels': 'datadiskinventory, file system; transferinventory, file '
                'system; videodiskinventory, file system'},
 {'new_label': 'media_type',
  'old_label': 'media type',
  'old_labels': 'datadiskinventory, type; transferinventory,type; '
                'videodiskinventory, media type; audiodiskinventory, media '
                'type'},
 {'new_label': 'operating_system_requirements',
  'old_label': 'operating system requirements',
  'old_labels': 'datadiskinventory, operating system requirements; '
                'audiodiskinventory, operating system requirements'},
 {'new_label': 'media_serial_ number\xa0\xa0\xa0',
  'old_label': 'serial/batch number',
  'old_labels': 'datadiskinventory, serial/batch number; transferinventory, '
                'serial/batch number; videodiskinventory, serial/batch number; '
                'audiodiskinventory, serial/batch number'},
 {'new_label': 'media_virtual_label',
  'old_label': 'virtual disk label',
  'old_labels': 'datadiskinventory, virtual disk label; audiodiskinventory, '
                'virtual disk label; videodiskinventory, virtual disk label'},
 {'new_label': 'media_case_label',
  'old_label': 'case or sleeve label',
  'old_labels': 'datadiskinventory, case or sleeve label; audiodiskinventory, '
                'case or sleeve label; videodiskinventory, case or sleeve '
                'label'},
 {'new_label': 'media_label',
  'old_label': 'physical label',
  'old_labels': 'datadiskinventory, physical label; audiodiskinventory, '
                'physical label; videodiskinventory, physical label'},
 {'new_label': 'transfer_mechanism',
  'old_label': 'transfer mechansim',
  'old_labels': 'transferinventory, transfer mechansim'},
 {'new_label': 'extraction_drive',
  'old_label': 'extraction drive used',
  'old_labels': 'datadiskinventory, extraction drive used'},
 {'new_label': 'date-imaged',
  'old_label': 'date imaged',
  'old_labels': 'datadiskinventory, date imaged; transferinventory, date '
                'imaged; audiodiskinventory, date imaged; videodiskinventory, '
                'date imaged'},
 {'new_label': 'disk_image_filename',
  'old_label': 'disk image filename/s',
  'old_labels': 'datadiskinventory, disk image filename/s; transferinventory, '
                'disk image filename/s; audiodiskinventory, disk image '
                'filename/s; videodiskinventory, disk image filename/s'},
 {'new_label': 'md5',
  'old_label': 'md5',
  'old_labels': 'datadiskinventory, disk image filename/s; transferinventory, '
                'disk image filename/s; audiodiskinventory, disk image MD5 '
                'hash; disk image MD5 hash; filelist, MD5'},
 {'new_label': 'disk_parts',
  'old_label': 'disk image number of parts',
  'old_labels': 'datadiskinventory, disk image number of parts; '
                'transferinventory, disk image number of parts; '
                'videodiskinventory, disk image number of parts'},
 {'new_label': 'disk_image_type',
  'old_label': 'disk image type',
  'old_labels': 'datadiskinventory, disk image type; transferinventory, image '
                'type; videodiskinventory, disk image type'},
 {'new_label': 'imaging_comments',
  'old_label': 'imaging comments',
  'old_labels': 'datadiskinventory, imaging comments; transferinventory, '
                'imaging comments; videodiskinventory, imaging comments'},
 {'new_label': 'extraction_hardware',
  'old_label': 'datadiskinventory; extraction drive used',
  'old_labels': 'datadiskinventory; extraction drive used'},
 {'new_label': 'Imaging_software',
  'old_label': 'imaging software used',
  'old_labels': 'datadiskinventory, imaging software used; transferinventory, '
                'imaging software used; videodiskinventory, imaging software '
                'used'},
 {'new_label': 'extraction_software',
  'old_label': 'extraction software used',
  'old_labels': 'audiodiskinventory, extraction software used'},
 {'new_label': 'imaging_status',
  'old_label': 'imaging status',
  'old_labels': 'datadiskinventory, imaging status; transferinventory, imaging '
                'status; videodiskinventory, imaging status'},
 {'new_label': 'extracted_disk_number_of_tracks',
  'old_label': 'extracted disk number of tracks',
  'old_labels': 'audiodiskinventory, extracted disk number of tracks'},
 {'new_label': 'extraction_status',
  'old_label': 'extraction status',
  'old_labels': 'audiodiskinventory, extraction Status'},
 {'new_label': 'Extraction comments',
  'old_label': 'extraction comments',
  'old_labels': 'audiodiskinventory, extraction Comments'},
 {'new_label': 'audio_file_format',
  'old_label': 'file format',
  'old_labels': 'audiodiskinventory, file format'},
 {'new_label': 'encoding_scheme',
  'old_label': 'encoding_scheme',
  'old_labels': 'audiodiskinventory, encoding_scheme'},
 {'new_label': 'sample_rate',
  'old_label': 'sample rate',
  'old_labels': 'audiodiskinventory, sample rate'},
 {'new_label': 'bit_depth',
  'old_label': 'bit depth',
  'old_labels': 'audiodiskinventory, bit depth'},
 {'new_label': 'bit_rate',
  'old_label': 'bit rate',
  'old_labels': 'audiodiskinventory, bit rate'},
 {'new_label': 'duration',
  'old_label': 'duration',
  'old_labels': 'audiodiskinventory, duration'},
 {'new_label': 'extracted_disk_folder_name',
  'old_label': 'extracted disk folder name',
  'old_labels': 'audiodiskinventory, extracted disk folder name'},
 {'new_label': 'date_extracted',
  'old_label': 'date extracted',
  'old_labels': 'audiodiskinventory, date extracted'},
 {'new_label': 'content_dates',
  'old_label': 'covering dates',
  'old_labels': 'datadiskinventory, covering dates; transferinventory, '
                'covering dates; audiodiskinventory, covering dates; '
                'videodiskinventory, covering dates'},
 {'new_label': 'content_genre',
  'old_label': 'genre',
  'old_labels': 'datadiskinventory, genre; transferinventory, genre; '
                'audiodiskinventory, genre; videodiskinventory, genre'},
 {'new_label': 'content_create_agent',
  'old_label': 'genre',
  'old_labels': 'datadiskinventory, contributors; transferinventory, '
                'contributors; audiodiskinventory, genre; videodiskinventory, '
                'genre'},
 {'new_label': 'content_scope',
  'old_label': '',
  'old_labels': 'datadiskinventory, scope and content; transferinventory, '
                'scope an content; audiodiskinventory, scope and content; '
                'videodiskinventory, '},
 {'new_label': 'content_rights',
  'old_label': 'rights',
  'old_labels': 'datadiskinventory, rights information; transferinventory, '
                'rights information; audiodiskinventory, rights; '
                'videodiskinventory, rights'},
 {'new_label': 'content_accessrestrict',
  'old_label': 'access restriction',
  'old_labels': 'datadiskinventory, access restrictions; transferinventory, '
                'access restrictions; audiodiskinventory, accessrestrictions; '
                'videodiskinventory, access restriction'}]


def get_file_path_list(acc_folder_path):
    list_of_files = list()
    for (dirpath, dirnames, filenames) in os.walk(acc_folder_path):
        list_of_files += [os.path.join(dirpath, file) for file in filenames]
    return list_of_files


def convert_acc_records_to_json(acc_file_path):
    """This takes the full file path incl file_name and the name of the
    worksheet of the accession file and returns a json obj."""
    excel_data_df = pd.read_excel(acc_file_path)
    records_str = excel_data_df.to_json(orient="records")
    records_in_json = json.loads(records_str)
    return records_in_json


def relabel_json(file_as_dict, list_of_keys):
    """
    this function firstly lowers all keys in the given dict to ensure that the
    old keys will match with the new ones. Then it iterates over all old keys
    and for every old key in the dict it updates a newly created dict to use
    the new keys instead of the old ones and takes the respective values.
    :param file_as_dict: this takes a dict, in this case a row which represents
    a file
    :param list_of_keys: this takes the cleaned up list of keys to map
    :return:
    """
    new_dict = {}
    file_as_dict = dict((k.lower(), v) for k, v in file_as_dict.items())
    for keypair in list_of_keys:
        if keypair["old_label"] in file_as_dict:
            try:
                new_dict.update({keypair["new_label"]: file_as_dict[keypair[
                    "old_label"]]})
            except KeyError:
                logging.info(f"It seems like the keypair {keypair} has no key "
                             f"'new_label'")
                continue
        else:
            logging.info(f"{keypair['old_label']} is not in the accession")
    return new_dict


def merge_records_to_dict(acc_rows, list_of_keys):
    """
    This merges the list of rows in accession (and thus the files in the
    accession) together to be displayed in a new dict. It therefore iterates
    over every file (row) executes the relabeling function and adds the
    relabeled file to the accesion file list which is the value of the new dict.
    :param list_of_rows: takes a list of the rows from the accession file.
    While a row is representing a file in the accession.
    :param list_of_keys: takes the cleaned up list of the keypairs to map
    :return: a dict, which represents the relabeled accession with a
    list of the files in it.

    """
    relabeled_dict = {"accession_name": None,
           "accession_files": []}
    for row in acc_rows:
        try:
            relabeled_dict["accession_name"] = row["Collection name"]
        except KeyError:
            logging.info(f"{row} has no Collection name and thus None is "
                         f"specified")
            continue
        relabeled_dict["accession_files"].append(relabel_json(row, list_of_keys))
    return relabeled_dict


def get_file_name(file_path, mapped_dict):
    if mapped_dict["accession_name"]:
        accession_name = mapped_dict["accession_name"]
        file_name = file_path + accession_name + ".json"
    else:
        file_name = file_path + "acc_not_specified" + ".json"
    return file_name


def write_relabeled_json(file_path, mapped_dict):
    """
    This writes the relabeled dict into a json file at the given path
    :param file_path: path where the json should be written to
    :param mapped_dict: the relabeled dict which should be written to the json
    :return:
    """
    file_name = get_file_name(file_path, mapped_dict)
    converted_md_object = json.dumps(mapped_dict, sort_keys=True)
    with open(file_name, "w") as f:
        f.write(converted_md_object)
        f.close()


def main(acc_folder_path, list_of_keys, output_file):
    """
    :return:
    """
    list_of_acc_files = get_file_path_list(acc_folder_path)
    if list_of_acc_files:
        for acc in list_of_acc_files:
            records_as_json = convert_acc_records_to_json(acc)
            merged_relabeled_records = merge_records_to_dict(records_as_json, list_of_keys)
            write_relabeled_json(output_file, merged_relabeled_records)
    else:
        raise Exception(f"It seems that there are no accession files in the "
                        f"folder {acc_folder_path}")


if __name__ == '__main__':
    parser = ArgumentParser(description="...")
    parser.add_argument("acc_folder_path", help="Base path where"
                                                "the accessions are stored")
    parser.add_argument("output_file", help="Write location of the new output")
    # list_of_keys is optional, so you can pass any list of keys you like to migrate
    parser.add_argument("-o", "--list_of_keys", default=LIST_OF_KEYS,
                        help="List of keys as a dict "
                             "with old and new labels, which "
                             "shall be mapped")
    args = parser.parse_args()
    main(args.acc_folder_path, args.list_of_keys, args.output_file)