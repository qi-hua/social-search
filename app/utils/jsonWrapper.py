# import Union
from typing import Union
import json

class JsonWrapper:
    def __init__(self, data: Union['JsonWrapper',dict,list,bool,str,int,float,None]):
        if isinstance(data, dict):
            self._data = {k: JsonWrapper(v) for k, v in data.items()}
        elif isinstance(data, list):
            self._data = [JsonWrapper(v) for v in data]
        else:
            self._data = data

    def __getattr__(self, item):
        return self._data[item]
    
    def __getitem__(self, item):
        return self._data[item]

    def __str__(self):
        return repr(self._data)
    
    def __repr__(self):
        # return repr(self._data)
        return json.dumps(self.to_json(), indent=4, ensure_ascii=False) if isinstance(self._data, dict|list) else str(self._data)
    
    def __iter__(self):
        return iter(self._data)
    
    def __len__(self):
        return len(self._data)
    
    def __contains__(self, item):
        return item in self._data
    
    def __eq__(self, other):
        return self._data == other
    
    def __ne__(self, other):
        return self._data != other
    
    def to_json(self):
        if isinstance(self._data, dict):
            return {k: v.to_json() if isinstance(v, JsonWrapper) else v for k, v in self._data.items()}
        elif isinstance(self._data, list):
            return [v.to_json() if isinstance(v, JsonWrapper) else v for v in self._data]
        return self._data
    

if __name__ == '__main__':
    # 示例JSON数据
    data = {
        "code": 200,
        "data": {
            "core": {
                "value": 42
            },
            "items": [
                {"name": "item1", "value": 1},
                {"name": "item2", "value": 2}
            ]
        }
    }

    # 将JSON数据包装成DictWrapper对象
    wrapped_data = JsonWrapper(data)

    # 像JavaScript一样读取属性
    print(wrapped_data.code)  # 输出: 200
    print(wrapped_data.data.core.value)  
    print(wrapped_data.data.items[0].name)  # 输出: item1
    print(wrapped_data.data.items[1].value)  # 输出: 2

    print(wrapped_data.to_json())