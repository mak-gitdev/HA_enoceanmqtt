import unittest
from pathlib import Path

import yaml

from enoceanmqtt.overlays.homeassistant.ha_communicator import custom_merge


class MappingTestCase(unittest.TestCase):

    def test_add_mapping(self):
        mapping_path = Path(__file__).parent.parent / 'enoceanmqtt' / 'overlays' / 'homeassistant' / 'mapping.yaml'
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping = yaml.safe_load(mapping_file)
        entity_to_add = {'component': "cover",
                         'name': "cover2",
                         'config': {}}
        extra_mapping = {
            0xD2: {
                0x05: {
                    0x00: {
                        'entities': {
                            'add':
                            [
                                entity_to_add,
                            ]
                        }
                    }
                }
            }
        }
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x05][0x00]['entities'])
        print(merged_mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue(entity_to_add in merged_mapping[0xD2][0x05][0x00]['entities'])  # add assertion here
        self.assertTrue(entity_to_add not in mapping[0xD2][0x05][0x00]['entities'])

    def test_remove_mapping(self):
        mapping_path = Path(__file__).parent.parent / 'enoceanmqtt' / 'overlays' / 'homeassistant' / 'mapping.yaml'
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping = yaml.safe_load(mapping_file)
        entity_to_add = {'component': "cover",
                         'name': "cover"}
        extra_mapping = {
            0xD2: {
                0x05: {
                    0x00: {
                        'entities': {
                            'remove':
                                [
                                    entity_to_add,
                                ]
                        }
                    }
                }
            }
        }
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x05][0x00]['entities'])
        print(merged_mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue(entity_to_add not in merged_mapping[0xD2][0x05][0x00]['entities'])  # add assertion here


if __name__ == '__main__':
    unittest.main()
