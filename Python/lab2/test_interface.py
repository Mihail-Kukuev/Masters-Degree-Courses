
import sys
import unittest
import importlib
import collections

try:
    import mock
except ImportError:
    try:
        from unittest import mock
    except ImportError:
        mock = None

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    str_type = basestring
    int_type = (int, long)
except NameError:
    str_type = str
    int_type = int


# uncomment the line below and change the path specified
# sys.path.insert(0, r'path_to_solution_folder')


class InterfaceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if mock is None:
            print('"mock" is not imported. cannot check stdout')

    def setUp(self):
        self._stdout_mock = self._setup_stdout_mock()

    def _setup_stdout_mock(self):
        if mock is None:
            return None

        patcher = mock.patch('sys.stdout', new=StringIO())
        patcher.start()
        self.addCleanup(patcher.stop)
        return patcher.new

    def _check_stdout_empty(self, file_name):
        if self._stdout_mock is not None:
            self.assertFalse(self._stdout_mock.getvalue(),
                             'no prints to console are allowed in "%s"' % file_name)

    def _load_function(self, task_idx, file_name, func_names):
        try:
            loaded_task = importlib.import_module(file_name)
        except ImportError:
            self.fail('cannot import task #%d solution - no file "%s"' % (task_idx, file_name))

        func_names = (func_names, ) if isinstance(func_names, str_type) else func_names
        loaded_functions = list(filter(None, (getattr(loaded_task, func_name, None) for func_name in func_names)))

        self.assertEqual(1, len(loaded_functions),
                         'cannot import task #%d solution - only one of function(-s) "%s" must be in file "%s"'
                         % (task_idx, file_name, func_names))

        return loaded_functions[0]

    def test_special_sum(self):
        f = self._load_function(0, 'special_sum', 'calculate_special_sum')
        self.assertIsInstance(f(1), int_type)
        self._check_stdout_empty('special_sum')

    def test_pythagoras(self):
        f = self._load_function(1, 'pythagoras', 'get_pythagoras_triples')
        self.assertIsInstance(f(1), collections.Iterable)
        self._check_stdout_empty('pythagoras')

    def test_primes(self):
        f = self._load_function(2, 'primes', 'get_primes')
        self.assertIsInstance(f(1), collections.Iterable)
        self._check_stdout_empty('primes')

    def test_unique(self):
        f = self._load_function(3, 'unique', ('compress', 'get_unique'))
        self.assertIsInstance(f([1]), list)
        self._check_stdout_empty('unique')

    def test_sort(self):
        f = self._load_function(4, 'merge_sort', 'sort')
        self.assertIsInstance(f([1]), list)
        self.assertIsInstance(f(tuple([1])), tuple)
        self._check_stdout_empty('merge_sort')


if __name__ == '__main__':
    unittest.main()
