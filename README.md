# About

A simple regression test framework (think personal autograder) for use on your EECS project. You can use it to organize and run you code against given inputs and compare the output for correctness. You can use it in your EECS projects, assuming of course that doing so does not violate the code use, or honor code restrictions, by which you MUST abide.

# Usage

First, clone the framework into your project folder:

    git clone https://github.com/michiganhackers/regression-test-framework.git
    
Second, create your testplan. 

Here is an example plan as a good starting point. 

    {
        "plan_name": "My test plan", 
        "output_file": "<thisValueIsNotUsedYet>", 
        "precompile_script": "make",
        "postrun_script": "make clean",
        "testplan": [
            {
                "test_name": "test1", 
                "build_script": "make test1", 
                "run_script": "./test1.out", 
                "correct_output": "correctOutput/test1.txt", 
                "timeout_warn": 5,
                "timeout_stop": 10 
            }
        ]
    }
Every value that ends in script will be executed as if it was a line you wrote in the terminal.

To run (defaults to testplan.plan if no arguments are given):

    python testplan.py <testplan.plan>

What you should see:

    NAME                RUNTIME (Seconds)   OUTPUT_CORRECT      SEGFAULT            TIMEOUT             
    genOutput           0.00805902481079    None                False               False               
    testCorrect         0.00782299041748    True                False               False               
    testIncorrect       0.00956702232361    False               False               False               
    testTimeOut         1.00118613243       None                False               True                
    testSegfault        0.00868511199951    None                False               False    



# Contributors
We (I) would love to get feedback on this, either via issue submissions, or viapull-requests. If you submit a pull-request, be sure to add your name to this list. 

+ Jonathan Meed <jonny2112@gmail.com>


# License
Copyright (C) 2014 Jonathan Meed <jonny2112@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
