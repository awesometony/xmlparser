# Summary
This script will find similar elements in two html pages based on similarities of argument values between elements.

# Requirements
Installed lxml module. To install it run

* `pip3 install lxml`

# How to run 

* `python3 main.py <path-to-original-html> <path-to-changed-html> <id of element to look for>`

Example:

* `python3 main.py /Users/user/test/startbootstrap-sb-admin-2-examples/sample-0-origin.html /Users/user/test/startbootstrap-sb-admin-2-examples/sample-2-container-and-clone.html make-everything-ok-button`

# Output
Xpath to the element in changed html file will be printed to the command line with some additional info.
