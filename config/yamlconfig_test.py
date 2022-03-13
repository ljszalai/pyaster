import unittest
from yamlconfig import YConfig


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.y_config = YConfig()

    def test_read(self):
        config = self.y_config.read('yamls', 'env-defaults.yml')
        self.assertEqual(config['erdecache']['redis']['ttl'], 300, "TTL shall be 300")

    def test_read_env_not_in_file(self):
        config = self.y_config.read_env_dict('yamls', 'dev')
        with self.assertRaises(KeyError) as raises:
            var = config['erdecache']['redis']['ttl']
            self.assertEqual(var, None)
        with self.assertRaises(KeyError) as raises:
            var = config['pyaster']['fitonly']
            self.assertEqual(var, None)

    def test_read_env_in_file(self):
        config = self.y_config.read_configuration('yamls', ['sandbox', 'dev'])
        print(config)
        self.assertEqual(config['pyaster']['tm4j']['environment'], 'Dev', "Environment shall be Dev")
        self.assertEqual(config['erdecache']['redis']['ttl'], 300, "TTL shall be 300")
        self.assertEqual(config['pyaster']['sandboxonly'], 'example', "sandboxonly shall be example")
        self.assertEqual(config['erdecache']['redis']['stream']['host'],
                         'dev-redis-stream.example.com', 'Stream host shall be the DEV one')

    def test_get_config(self):
        y_config = YConfig('yamls', ['sandbox', 'dev'])
        self.assertEqual(y_config.get('pyaster.tm4j.environment'), 'Dev', "Environment shall be Dev")
        self.assertEqual(y_config.get('erdecache.redis.ttl'), 300, "TTL shall be 300")
        self.assertEqual(y_config.get('pyaster.sandboxonly'), 'example', "sandboxonly shall be example")
        self.assertEqual(y_config.get('erdecache.redis.stream.host'),
                         'dev-redis-stream.example.com', 'Stream host shall be the DEV one')


if __name__ == '__main__':
    unittest.main()
