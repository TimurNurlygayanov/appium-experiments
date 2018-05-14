Inroduction
-----------
This repository contains simple examples how we can use appium in mobile testing.

Please start with install_appium_mac.sh script.


How To Find Locators
--------------------

UI tool to detect the locators of elements:

    /Users/<user>/Library/Android/sdk/tools/bin/uiautomatorviewer


Get App ID and Activity Name
----------------------------

This command allows to get active app id and activity name (open app manually first):

    adb shell "dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'"

