import importlib, inspect
importlib.invalidate_caches()
mod = importlib.import_module('app.services.deduction_service')
print('module file:', mod.__file__)
print('\n'.join(inspect.getsource(mod).splitlines()[:20]))
