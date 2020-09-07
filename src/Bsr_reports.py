'''
Created on Nov 17, 2019

@author: DELL
'''
from Object_repository import driver as driver
from Object_repository import LaunchBrowser
from Object_repository import Teardown as TearDown
import HtmlTestRunner
import unittest


class Test(unittest.TestCase):
    def setUp(self):
        LaunchBrowser(self)
        
    def testLaunch(self):
        print(driver.current_url)
    def testVerify_res(self):
        pass
    
    def testvalidate(self):
        pass
    
    def tearDown(self):
        TearDown(self)

        
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="C:/Users/DELL/git/Bse_Extractor/bsetestresults",report_title="Test Reports", report_name="Functional"))
    