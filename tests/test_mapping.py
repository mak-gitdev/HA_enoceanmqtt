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
                        'entities':
                            [
                                entity_to_add,
                            ]
                    }
                }
            }
        }
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x05][0x00]['entities'])
        print(merged_mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue(entity_to_add in merged_mapping[0xD2][0x05][0x00]['entities'])  # add assertion here
        self.assertTrue(entity_to_add not in mapping[0xD2][0x05][0x00]['entities'])

    def test_add_mapping_2(self):
        mapping_path = Path(__file__).parent.parent / 'enoceanmqtt' / 'overlays' / 'homeassistant' / 'mapping.yaml'
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping = yaml.safe_load(mapping_file)
        entity_to_add = {'component': "cover",
                         'name': "cover2",
                         'config': {},
                         'action': 'add'}
        extra_mapping = {
            0xD2: {
                0x05: {
                    0x00: {
                        'entities':
                            [
                                entity_to_add,
                            ]
                    }
                }
            }
        }
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x05][0x00]['entities'])
        print(merged_mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue(entity_to_add in merged_mapping[0xD2][0x05][0x00]['entities'])  # add assertion here
        self.assertTrue(entity_to_add not in mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue('state' not in merged_mapping[0xD2][0x05][0x00]['entities'][-1])

    def test_add_identical_mapping(self):
        mapping_path = Path(__file__).parent.parent / 'enoceanmqtt' / 'overlays' / 'homeassistant' / 'mapping.yaml'
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping = yaml.safe_load(mapping_file)
        entity_to_add = {'component': "cover",
                         'name': "cover",
                         'added_key': 'added_value',
                         'action': 'add'}
        extra_mapping = {
            0xD2: {
                0x05: {
                    0x00: {
                        'entities':
                            [
                                entity_to_add,
                            ]
                    }
                }
            }
        }
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x05][0x00]['entities'])
        print(merged_mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue((entity_to_add | mapping[0xD2][0x05][0x00]['entities'][0]) in merged_mapping[0xD2][0x05][0x00]['entities'])  # add assertion here
        self.assertTrue(entity_to_add not in mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue('action' not in merged_mapping[0xD2][0x05][0x00]['entities'][-1])

    def test_remove_mapping(self):
        mapping_path = Path(__file__).parent.parent / 'enoceanmqtt' / 'overlays' / 'homeassistant' / 'mapping.yaml'
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping = yaml.safe_load(mapping_file)
        entity_to_remove = {'component': "cover",
                            'name': "cover",
                            'action': 'remove'}
        extra_mapping = {
            0xD2: {
                0x05: {
                    0x00: {
                        'entities':
                            [
                                entity_to_remove,
                            ]
                    }
                }
            }
        }
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x05][0x00]['entities'])
        print(merged_mapping[0xD2][0x05][0x00]['entities'])
        self.assertTrue(entity_to_remove not in merged_mapping[0xD2][0x05][0x00]['entities'])  # add assertion here

    def test_file_mapping(self):
        mapping_path = Path(__file__).parent.parent / 'enoceanmqtt' / 'overlays' / 'homeassistant' / 'mapping.yaml'
        extra_mapping_path = Path(__file__).parent / 'resources' / 'extra_mapping.yaml'
        with open(mapping_path, 'r', encoding='utf-8') as mapping_file:
            mapping = yaml.safe_load(mapping_file)
        with open(extra_mapping_path, 'r', encoding='utf-8') as mapping_file:
            extra_mapping = yaml.safe_load(mapping_file)
        merged_mapping = custom_merge(mapping, extra_mapping)
        print(mapping[0xD2][0x01][0x01]['entities'])
        print(merged_mapping[0xD2][0x01][0x01]['entities'])
        names = [entity['name'] for entity in merged_mapping[0xD2][0x01][0x01]['entities']]
        self.assertTrue("switch2" in names)
        self.assertTrue("query_status" not in names)


if __name__ == '__main__':
    unittest.main()
