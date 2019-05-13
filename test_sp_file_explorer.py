import sp_file_explorer
from logging import INFO, DEBUG, WARN, getLogger
from unittest import TestCase, main
from os import getcwd, listdir
from os.path import isfile, join


class TestLogger(TestCase):

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

    def test_log_file_existance(self):
        path = join(getcwd(), self.logfile)
        self.assertTrue(isfile(path))

class TestBasicReducerGetInitState(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = sp_file_explorer.BasicReducers.getInitState()

    def test_state_keys(self):
        self.assertTrue("directory" in self.state)
        self.assertTrue("children" in self.state)
        self.assertTrue("selected" in self.state)
        self.assertTrue("scroll_data" in self.state)
        self.assertTrue("prompt_data" in self.state)
        self.assertTrue("mode" in self.state)
        self.assertTrue("text" in self.state)

    def test_scroll_data_keys(self):
        self.assertTrue("list_size" in self.state["scroll_data"])
        self.assertTrue("list_width" in self.state["scroll_data"])
        self.assertTrue("scroll_trigger" in self.state["scroll_data"])
        self.assertTrue("scroll_top" in self.state["scroll_data"])

    def test_prompt_data_keys(self):
        self.assertTrue("cmd_prompt" in self.state["prompt_data"])
        self.assertTrue("brs_prompt" in self.state["prompt_data"])   

    def test_directory(self):
        self.assertEqual(self.state["directory"], getcwd())

    def test_children(self):
        self.assertEqual(self.state["children"], listdir(getcwd()))
    
    def test_selected(self):
        self.assertEqual(len(self.state["selected"]), 1)
        self.assertTrue(self.state["selected"][0] in self.state["children"])
        self.assertEqual(self.state["children"].index(self.state["selected"][0]), 0)    
    def test_scroll_data(self):
        data = self.state["scroll_data"]
        self.assertEqual(data["list_size"], 40)
        self.assertEqual(data["list_width"], 100)
        self.assertEqual(data["scroll_trigger"], 3)
        self.assertEqual(data["scroll_top"], 0)

    def test_prompt_data(self):
        data = self.state["prompt_data"]
        self.assertEqual(data["cmd_prompt"], "(Command):")
        self.assertEqual(data["brs_prompt"], "(Browse) ")

    def test_mode(self):
        self.assertEqual(self.state["mode"], "browse")

    def test_text(self):
        self.assertEqual(self.state["text"], "(Browse) SP File Explorer")


class TestBasicReducerSameState(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = sp_file_explorer.BasicReducers.getInitState()
        self.newState = sp_file_explorer.BasicReducers.sameState(self.state) 

    def test_copied_state_keys(self):
        for key in self.state:
            self.assertTrue(key in self.newState)

    def test_copied_scroll_data_keys(self):
        for key in self.state["scroll_data"]:
            self.assertTrue(key in self.newState["scroll_data"])

    def test_copied_prompt_data_keys(self):
        for key in self.state["prompt_data"]:
            self.assertTrue(key in self.newState["prompt_data"])

    def test_deep_copy_state(self):
        self.assertFalse(self.newState is self.state)

    def test_deep_copy_scroll_data(self):
        self.assertFalse(self.newState["scroll_data"] is self.state["scroll_data"])    
    
    def test_deep_copy_prompt_data(self):
        self.assertFalse(self.newState["prompt_data"] is self.state["prompt_data"])

    def test_copied_prompt_data_values(self):
        for key in self.state["prompt_data"]:
            self.assertEqual(self.state["prompt_data"][key], self.newState["prompt_data"][key])

    def test_copied_scroll_data_values(self):
        for key in self.state["scroll_data"]:
            self.assertEqual(self.state["scroll_data"][key], self.newState["scroll_data"][key])

    def test_copied_state_values(self):
        for key in self.state:
            self.assertEqual(self.state[key], self.newState[key])

    def test_copied_state(self):
        self.assertEqual(self.state, self.newState)

class TestBasicReducerChangeModeToBrowse(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = sp_file_explorer.BasicReducers.getInitState()
        self.state["mode"] = "command"
        self.state["text"] = "(Command):blah"
        self.brs_text = "test"
        self.newState = sp_file_explorer.BasicReducers.changeModeToBrowse(self.state, self.brs_text) 
    
    def test_deep_copy_state(self):
        self.assertFalse(self.newState is self.state)

    def test_deep_copy_scroll_data(self):
        self.assertFalse(self.newState["scroll_data"] is self.state["scroll_data"])    
    
    def test_deep_copy_prompt_data(self):
        self.assertFalse(self.newState["prompt_data"] is self.state["prompt_data"])

    def test_state_mode(self):
        self.assertEqual(self.state["mode"], "command")
        self.assertEqual(self.newState["mode"], "browse")

    def test_state_text(self):
        self.assertEqual(self.state["text"], "(Command):blah")
        self.assertEqual(self.newState["text"], "(Browse) test")

    def test_copied_prompt_data_values(self):
        for key in self.state["prompt_data"]:
            self.assertEqual(self.state["prompt_data"][key], self.newState["prompt_data"][key])

    def test_copied_scroll_data_values(self):
        for key in self.state["scroll_data"]:
            self.assertEqual(self.state["scroll_data"][key], self.newState["scroll_data"][key])

    def test_copied_state_other_keys(self):
        for key in self.state:
            if key != "mode" and key != "text":
                self.assertEqual(self.state[key], self.newState[key])

if __name__ == "__main__":
    main(verbosity=2)
