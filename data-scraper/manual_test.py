from manual_testing.okidoki_test import OkidokiTest
from manual_testing.soov_test import SoovTest
from manual_testing.hv_test import HvTest
from dotenv import load_dotenv
load_dotenv(override=True)
#okidoki_test = OkidokiTest()
#okidoki_test.start('https://www.okidoki.ee/item/iphone-14-pro/13160364/')

#soov_test = SoovTest()
#soov_test.start('https://soov.ee/25717198-iphone-13-pro-gold-128gb/details.html')

hv_test = HvTest()
hv_test.start('https://foorum.hinnavaatlus.ee/viewtopic.php?t=856945')