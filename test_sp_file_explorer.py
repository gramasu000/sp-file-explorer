import sp_file_explorer
from logging import INFO, DEBUG, getLogger
from unittest import TestCase, main
from os import getcwd, listdir

sp_file_explorer.LOGGER = getLogger(__name__).setLevel(

class LoggerTestCase(TestCase):

    def setUp(self):
        self.logname = "_test"
        self.logfile = "_test"
        self.logger = sp_file_explorer.initLogging(self.logname, self.logfile)
    
    def test_logger_level(self):
        self.assertEqual(self.logger.getEffectiveLevel(), DEBUG)
        
    def test_logger_string(self):
        self.assertEqual(self.logger.__str__(), f"<Logger {self.logname} (DEBUG)>") 

    def test_logger_handlers(self):
        self.assertTrue(self.logger.hasHandlers())
        self.assertEqual(len(self.logger.handlers), 2)
        
    def test_handler0_string(self):
        self.assertEqual(self.logger.handlers[0].__str__(), "<StreamHandler <stderr> (INFO)>")

    def test_handler1_string(self):
        self.assertEqual(self.logger.handlers[1].__str__(), f"<FileHandler {getcwd()}/{self.logfile} (DEBUG)>")

class ReducerGetInitStateTestCase(TestCase):
    
    def setUp(self):
        self.state = sp_file_explorer.Reducers.getInitState()

    def state_keys(self):
        self.assertTrue("directory" in self.state)
        self.assertTrue("children" in self.state)
        self.assertTrue("selected" in self.state)
        self.assertTrue("scroll_data" in self.state)
        self.assertTrue("mode" in self.state)
        self.assertTrue("text" in self.state)
        self.assertFalse("something_weird" in self.state)
        self.assertFalse("list_size" in self.state)
        self.assertFalse("list_width" in self.state)
        self.assertFalse("scroll_trigger" in self.state)
        self.assertFalse("scroll_top" in self.state)
        self.assertTrue("list_size" in self.state["scroll_data"])
        self.assertTrue("list_width" in self.state["scroll_data"])
        self.assertTrue("scroll_trigger" in self.state["scroll_data"])
        self.assertTrue("scroll_top" in self.state["scroll_data"])

    def test_directory(self):
        self.assertEqual(self.state["directory"], getcwd())

    def test_children(self):
        self.assertEqual(self.state["children"], listdir(getcwd()))
    
    def test_selected(self):
        self.assertEqual(len(self.state["selected"]), 1)
        self.assertEqual(self.state["children"].index(self.state["selected"][0]), 0)
    
    def test_scroll_data(self):
        data = self.state["scroll_data"]
        self.assertEqual(data["list_size"], 40)
        self.assertEqual(data["list_width"], 100)
        self.assertEqual(data["scroll_trigger"], 3)
        self.assertEqual(data["scroll_top"], 0)

    def test_mode(self):
        self.assertEqual(self.state["mode"], "browse")

    def test_text(self):
        self.assertEqual(self.state["text"], "SP File Explorer")

if __name__ == "__main__":
    main(verbosity=2)
