# Author: Human beings feat. ChatGPT with GitHub Copilot
class FuzzDb():
    def __init__(self, fuzzdb_path: str):
        fuzzlist = self._load_fuzzdb(fuzzdb_path)
        intfloat = self._get_intfloat(fuzzlist)
        fuzzlist.extend(intfloat)
        self.fuzzlist = fuzzlist

    def _load_fuzzdb(self, fuzzdb_path: str):
        try:
            with open(fuzzdb_path, 'r') as f:
                lines = f.readlines()
                return [line.strip() for line in lines if line.strip()]
        except FileNotFoundError:
            print(f"Error: The file {fuzzdb_path} does not exist.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def _get_intfloat(self, fuzzlist):
        intfloat = []
        for item in fuzzlist:
            try:
                value = float(item)
                if value.is_integer() and not '.' in item:
                    intfloat.append(int(value))
                else:
                    intfloat.append(float(value))
            except ValueError:
                continue

        return intfloat
    
    def get_fuzzlist(self):
        return self.fuzzlist