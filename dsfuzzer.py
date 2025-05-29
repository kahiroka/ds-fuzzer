# Author: Human beings feat. ChatGPT with GitHub Copilot
class DsFuzzer():
    def fuzz(self, data, fuzz_value):
        results = []

        def _fuzz(current_data, path=None):
            if path is None:
                path = []

            if isinstance(current_data, dict):
                for key, value in current_data.items():
                    new_path = path + [key]
                    _fuzz(value, new_path)
            elif isinstance(current_data, list):
                for index, item in enumerate(current_data):
                    new_path = path + [index]
                    _fuzz(item, new_path)
            else:
                if fuzz_value != current_data:
                    new_data = _deep_copy(data)
                    _replace_at_path(new_data, path, fuzz_value)
                    results.append((new_data, path))

        def _deep_copy(obj):
            if isinstance(obj, dict):
                return {k: _deep_copy(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_deep_copy(item) for item in obj]
            else:
                return obj

        def _replace_at_path(obj, path, new_value):
            if not path:
                return new_value

            current = path[0]
            if len(path) == 1:
                if isinstance(obj, dict):
                    obj[current] = new_value
                elif isinstance(obj, list):
                    obj[current] = new_value
            else:
                if isinstance(obj, dict):
                    obj[current] = _replace_at_path(obj[current], path[1:], new_value)
                elif isinstance(obj, list):
                    obj[current] = _replace_at_path(obj[current], path[1:], new_value) 
            return obj

        _fuzz(data)
        return results
