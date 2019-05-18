import sp_file_explorer
from logging import INFO, DEBUG, WARN, getLogger
from unittest import TestCase, main
from os import getcwd, listdir
from os.path import isfile, isdir, join, dirname
from pathlib import Path 
import string
import random

class RandomState: 

    @classmethod
    def getRandomString(cls):
        length = random.randint(0, 20)
        chars = string.ascii_letters + string.digits
        str = "".join(random.choice(chars) for i in range(length))
        return str

    @classmethod
    def getRandomDir(cls):
        num_dirs = random.randint(0,3)
        dir = str(Path.home())
        for i in range(num_dirs-1):
            children = [child for child in listdir(dir) if isdir(child)]
            if len(children) != 0:
                child = random.choice(children)
                dir = join(dir, child)
            else:
                break
        if len(listdir(dir)) != 0:
            return dir
        else:
            return dirname(dir) 

    @classmethod
    def getRandomSubset(cls, list):
        length = random.randint(0, len(list))
        sub_list = random.sample(list, length)
        return sub_list

    @classmethod
    def getRandomState(cls):
        newState = {}
        newState["directory"] = cls.getRandomDir()
        newState["children"] = listdir(newState["directory"])
        newState["selected"] = cls.getRandomSubset(newState["children"])
        newState["scroll_data"] = {
            "list_size": random.randint(0, 100),
            "list_width": random.randint(0, 100),
            "scroll_trigger": random.randint(0, 100),
            "scroll_top": random.randint(0, 100)
        }
        newState["prompt_data"] = {
            "cmd_prompt": cls.getRandomString(),
            "brs_prompt": cls.getRandomString()
        }
        newState["mode"] = random.choice(["browse", "command"])
        newState["text"] = cls.getRandomString()
        return newState


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
        self.state = sp_file_explorer.BasicReducer.getInitState()

    def test_state_keys(self):
        self.assertIn("directory", self.state)
        self.assertIn("children", self.state)
        self.assertIn("selected", self.state)
        self.assertIn("scroll_data", self.state)
        self.assertIn("prompt_data", self.state)
        self.assertIn("mode", self.state)
        self.assertIn("text", self.state)

    def test_scroll_data_keys(self):
        self.assertIn("list_size", self.state["scroll_data"])
        self.assertIn("list_width", self.state["scroll_data"])
        self.assertIn("scroll_trigger", self.state["scroll_data"])
        self.assertIn("scroll_top", self.state["scroll_data"])

    def test_prompt_data_keys(self):
        self.assertIn("cmd_prompt", self.state["prompt_data"])
        self.assertIn("brs_prompt", self.state["prompt_data"])   

    def test_directory(self):
        self.assertEqual(self.state["directory"], getcwd())

    def test_children(self):
        self.assertEqual(self.state["children"], listdir(getcwd()))
    
    def test_selected(self):
        self.assertEqual(len(self.state["selected"]), 1)
        self.assertIn(self.state["selected"][0], self.state["children"])
        self.assertEqual(self.state["children"].index(self.state["selected"][0]), 0)    

    def test_scroll_data(self):
        data = self.state["scroll_data"]
        self.assertEqual(data["list_size"], 25)
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
        self.state = RandomState.getRandomState()
        self.newState = sp_file_explorer.BasicReducer.sameState(self.state) 

    def test_copied_state_keys(self):
        for key in self.state:
            self.assertIn(key, self.newState)

    def test_copied_scroll_data_keys(self):
        for key in self.state["scroll_data"]:
            self.assertIn(key, self.newState["scroll_data"])

    def test_copied_prompt_data_keys(self):
        for key in self.state["prompt_data"]:
            self.assertIn(key, self.newState["prompt_data"])

    def test_deep_copy_state(self):
        self.assertIsNot(self.newState, self.state)

    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.newState["scroll_data"], self.state["scroll_data"])    
    
    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.newState["prompt_data"], self.state["prompt_data"])

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


class TestBasicReducerSetModeToBrowse(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = RandomState.getRandomState()
        self.brs_text = "test"
        self.newState = sp_file_explorer.BasicReducer.setModeToBrowse(self.state, self.brs_text) 
    
    def test_deep_copy_state(self):
        self.assertIsNot(self.newState, self.state)

    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.newState["scroll_data"], self.state["scroll_data"])    
    
    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.newState["prompt_data"], self.state["prompt_data"])

    def test_state_mode(self):
        self.assertEqual(self.newState["mode"], "browse")

    def test_state_text(self):
        self.assertEqual(self.newState["text"], self.newState["prompt_data"]["brs_prompt"] + self.brs_text)

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


class TestBasicReducerSetModeToCommand(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = RandomState.getRandomState()
        self.cmd_text = "test"
        self.newState = sp_file_explorer.BasicReducer.setModeToCommand(self.state, self.cmd_text) 

    def test_deep_copy_state(self):
        self.assertIsNot(self.newState, self.state)

    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.newState["scroll_data"], self.state["scroll_data"])    
    
    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.newState["prompt_data"], self.state["prompt_data"])

    def test_state_mode(self):
        self.assertEqual(self.newState["mode"], "command")

    def test_state_text(self):
        self.assertEqual(self.newState["text"], self.newState["prompt_data"]["cmd_prompt"] + self.cmd_text)

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


class TestBasicReducerDeleteText(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = RandomState.getRandomState()
        while len(self.state["text"]) == 0:
            self.state = RandomState.getRandomState()
        self.newState = sp_file_explorer.BasicReducer.deleteText(self.state)

    def test_deep_copy_state(self):
        self.assertIsNot(self.state, self.newState)
    
    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.state["scroll_data"], self.newState["scroll_data"])

    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.state["prompt_data"], self.newState["scroll_data"])

    def test_state_text(self):
        length = len(self.state["text"])
        newLength = len(self.newState["text"])
        self.assertIn(self.newState["text"], self.state["text"])
        self.assertEqual(length-1, newLength)
        self.assertEqual(self.newState["text"], self.state["text"][:newLength])
    
    def test_copied_prompt_data_values(self):
        for key in self.state["prompt_data"]:
            self.assertEqual(self.state["prompt_data"][key], self.newState["prompt_data"][key])

    def test_copied_scroll_data_values(self):
        for key in self.state["scroll_data"]:
            self.assertEqual(self.state["scroll_data"][key], self.newState["scroll_data"][key])

    def test_copied_state_other_keys(self):
        for key in self.state:
            if key != "text":
                self.assertEqual(self.state[key], self.newState[key])    


class TestBasicReducerAddText(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = RandomState.getRandomState()
        self.char = random.choice(string.ascii_letters + string.digits)
        self.newState = sp_file_explorer.BasicReducer.addText(self.state, self.char)

    def test_deep_copy_state(self):
        self.assertIsNot(self.state, self.newState)
    
    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.state["scroll_data"], self.newState["scroll_data"])

    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.state["prompt_data"], self.newState["scroll_data"])

    def test_state_text(self):
        length = len(self.state["text"])
        newLength = len(self.newState["text"])
        self.assertIn(self.state["text"], self.newState["text"])
        self.assertEqual(length+1, newLength)
        self.assertEqual(self.state["text"], self.newState["text"][:length])
        self.assertEqual(self.char, self.newState["text"][length:])
    
    def test_copied_prompt_data_values(self):
        for key in self.state["prompt_data"]:
            self.assertEqual(self.state["prompt_data"][key], self.newState["prompt_data"][key])

    def test_copied_scroll_data_values(self):
        for key in self.state["scroll_data"]:
            self.assertEqual(self.state["scroll_data"][key], self.newState["scroll_data"][key])

    def test_copied_state_other_keys(self):
        for key in self.state:
            if key != "text":
                self.assertEqual(self.state[key], self.newState[key])    


class TestBasicReducerMoveDir(TestCase):

    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = RandomState.getRandomState()
        self.newDir = RandomState.getRandomDir()
        self.newState = sp_file_explorer.BasicReducer.moveDir(self.state, self.newDir)

    def test_deep_copy_state(self):
        self.assertIsNot(self.state, self.newState)
    
    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.state["scroll_data"], self.newState["scroll_data"])

    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.state["prompt_data"], self.newState["scroll_data"])

    def test_dir(self):
        self.assertEqual(self.newState["directory"], self.newDir)
    
    def test_children(self):
        for i, key in enumerate(listdir(self.newDir)):
            self.assertIn(key, self.newState["children"])
            self.assertEqual(key, self.newState["children"][i])
    
    def test_selected(self):
        self.assertEqual(len(self.newState["selected"]), 0)

    def test_copied_prompt_data(self):
        for key in self.state["prompt_data"]:
            self.assertEqual(self.newState["prompt_data"][key], self.state["prompt_data"][key])

    def test_copied_scroll_data(self):
        for key in self.state["scroll_data"]:
            if key != "scroll_top":
                self.assertEqual(self.newState["scroll_data"][key], self.state["scroll_data"][key])     

    def test_copied_other(self):
        for key in self.state:
            if key not in ["directory", "children", "selected"]:
                self.assertEqual(self.newState[key], self.state[key])


class BasicReducerMoveSelection(TestCase):
    
    def setUp(self):
        sp_file_explorer.LOGGER = getLogger()
        sp_file_explorer.LOGGER.setLevel(WARN)
        self.state = RandomState.getRandomState()
        self.num_children = len(self.state["children"])
        self.indices = random.sample(range(self.num_children), random.randint(1, 10))
        self.newState = sp_file_explorer.BasicReducer.moveSelection(self.state, self.indices)

    def test_deep_copy_state(self):
        self.assertIsNot(self.state, self.newState)
    
    def test_deep_copy_scroll_data(self):
        self.assertIsNot(self.state["scroll_data"], self.newState["scroll_data"])

    def test_deep_copy_prompt_data(self):
        self.assertIsNot(self.state["prompt_data"], self.newState["scroll_data"])

    def test_selection_1(self):
        for i in self.indices:
            self.assertIn(self.state["children"][i], self.state["selected"])

    def test_selection_2(self):
        for i in range(self.num_children):         
            if i not in self.indices:
                self.assertNotIn(self.state["children"][i], self.state["selected"])

    def test_copied_prompt_data(self):
        for key in self.state["prompt_data"]:
            self.assertEqual(self.newState["prompt_data"][key], self.state["prompt_data"][key])

    def test_copied_scroll_data(self):
        for key in self.state["scroll_data"]:
            if key != "scroll_top":
                self.assertEqual(self.newState["scroll_data"][key], self.state["scroll_data"][key])     

    def test_copied_other(self):
        for key in self.state:
            if key not in ["selected"]:
                self.assertEqual(self.newState[key], self.state[key])


if __name__ == "__main__":
    main(verbosity=2)
