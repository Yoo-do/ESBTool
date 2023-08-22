import json
import os
import jsonschema


class JsonSchemaType:
    def __init__(self, name, json_data: dict = None, schema: dict = None):
        self.name = name
        if json_data is not None:
            self.schema = self.generate_jsonschema(json_data)
        else:
            self.schema = schema

    def validate(self, json_data: dict):
        try:
            jsonschema.validate(json_data, self.schema)
            return True
        except jsonschema.ValidationError as e:
            print(list(e.path).__str__() + ' : ' + e.message.__str__())
            return False
        except Exception as e:
            print(e.__str__())
            return False

    @staticmethod
    def generate_jsonschema(json_data):
        """生成jsonschema"""

        def get_type(data):
            if isinstance(data, dict):
                return 'object'
            elif isinstance(data, list):
                return 'array'
            elif isinstance(data, int):
                return 'integer'
            elif isinstance(data, float):
                return 'number'
            elif isinstance(data, str):
                return 'string'
            elif isinstance(data, bool):
                return 'boolean'

        result = {}
        properties = {}
        required = []
        if isinstance(json_data, dict):
            result.update({'type': get_type(json_data)})
            for key, val in json_data.items():
                required.append(key)
                if isinstance(val, dict):
                    properties.update({key: JsonSchemaType.generate_jsonschema(val)})
                elif isinstance(val, list):
                    properties.update({key: JsonSchemaType.generate_jsonschema(val)})
                else:
                    properties.update(
                        {key: {'type': get_type(val), 'tittle': val.__str__(), 'description': '', 'require': True}})

            result.update({'properties': properties})
            result.update({'required': required})

        elif isinstance(json_data, list):
            result.update({'type': get_type(json_data)})
            if len(json_data) > 0:
                result.update({'items': JsonSchemaType.generate_jsonschema(json_data[0])})

        return result

    def save(self):
        with open('../Models/' + self.name + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.schema, f, ensure_ascii=False)