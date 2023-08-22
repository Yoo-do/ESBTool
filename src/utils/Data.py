import json
import jsonschema
import FileIO


class Model:
    def __init__(self, model_name: str, model: dict):
        self.model_name = model_name
        self.model = model

    def validate(self, data: dict) -> bool:
        try:
            jsonschema.validate(data, self.model)
            return True
        except jsonschema.ValidationError as e:
            raise Exception(e.path).__str__() + ' : ' + e.message.__str__()

class Api(Model):
    def __init__(self, model_name: str, model: dict):
        super().__init__(model_name, model)




class Proj:
    def __init__(self, proj_name):
        self.proj_name = proj_name
        self.models = []
        self.apis = []

        self.fresh_models()
        self.fresh_apis()

    def fresh_models(self):
        """
        获取全部模型
        """
        models = FileIO.ProjIO.get_models(self.proj_name)
        for model in models:
            self.models.append(Model(model['model_name'], model['model']))

    def fresh_apis(self):
        """
        获取全部接口信息
        """
        pass


    def export_file(self):
        pass

if __name__ == '__main__':
    proj = Proj('检查系统')
    for model in proj.models:
        print(model.model_name)
        print(model.model)