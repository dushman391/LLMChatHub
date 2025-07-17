import os
import sys
import types
import tempfile
import unittest

# Provide stub modules for missing dependencies so ``import app`` succeeds even
# without the real packages installed.
sys.modules.setdefault('gradio', types.ModuleType('gradio'))
lc_stub = types.ModuleType('langchain_openai')
lc_stub.AzureChatOpenAI = object
sys.modules.setdefault('langchain_openai', lc_stub)
sys.modules.setdefault('requests', types.ModuleType('requests'))

import app

class SaveLoadTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.old_cwd = os.getcwd()
        os.chdir(self.tmpdir.name)
        app.conversation_history = [("User", "Hello"), ("AI", "Hi")]

    def tearDown(self):
        os.chdir(self.old_cwd)
        self.tmpdir.cleanup()

    def test_saved_file_appears_in_list(self):
        filename = 'test_chat.json'
        app.save_conversation(filename)
        self.assertIn(filename, app.get_saved_conversations())
        loaded = app.load_conversation(filename)
        self.assertEqual(loaded, app.conversation_history)

if __name__ == '__main__':
    unittest.main()
