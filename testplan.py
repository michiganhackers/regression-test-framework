import os
import subprocess
import os.path
import time
import json
import threading
import sys


class Cmd:
	def __init__(self, cmd, timeout): 
		self.process = None
		self.output =  "a"
		self.outputCorrect = False
		start = time.time()
		self.runCmd(cmd, timeout)
		end = time.time()
		self.returncode = self.process.returncode
		self.runtime = end - start
		self.output = self.output[0]



	def runCmd(self, cmd, timeout):
		def target():
			self.process = subprocess.Popen(cmd, shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT)
			self.output = self.process.communicate()
		thread = threading.Thread(target=target)
		thread.start()
		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()



class Testplan:
	def __init__(self, plan_name, output_file="tests.out", precompile_script=""):
		self.plan_name = plan_name
		self.output_file = output_file
		self.precompile_script = precompile_script
		self.testplan = []

	def decodeJson(self, jsn): # deserialize Testplan from json
		data = json.loads(jsn)
		self.plan_name = data["plan_name"]
		self.output_file = data["output_file"]
		self.precompile_script = data["precompile_script"]
		for testcase in data["testplan"]:
			case = Testcase("", "", "", "")
			case.decodeJson(testcase)
			self.testplan.append(case)

	def encodeJson(self):
		data = {
			'plan_name':self.plan_name,
			'output_file':self.output_file,
			'precompile_script':self.precompile_script,
			'testplan':[]
		}
		for test in self.testplan:
			data['testplan'].append(test.__dict__)
			print(test.encodeJson())
		return json.dumps(data,  indent=4, sort_keys=True)


	def precompile(self):
		if not os.path.exists("tmp"):
				os.makedirs("tmp")
		Cmd(self.precompile_script, 60)


	def compile(self):		
		for test in self.testplan:
			test.compile()

	def run(self):
		for test in self.testplan:
			test.run()
			
	def executePlan(self):
		self.precompile();
		self.compile();
		self.run();

	def addTestcase(self, testcase):
		self.testplan.append(testcase)



class Testcase:

	def __init__(self, test_name, build_script, run_script, correct_output, timeout_warn = 10, timeout_stop = 10):
		self.test_name = test_name
		self.build_script = build_script
		self.run_script = run_script
		self.correct_output = correct_output
		self.timeout_warn = timeout_warn
		self.timeout_stop = timeout_stop

	def decodeJson(self, jsn):
		self.test_name = jsn["test_name"]
		self.build_script = jsn["build_script"]
		self.run_script = jsn["run_script"]
		self.correct_output = jsn["correct_output"]
		self.timeout_warn = jsn["timeout_warn"]
		self.timeout_stop = jsn["timeout_stop"]

	def encodeJson(self):
		data = {
			'test_name': self.test_name,
			'build_script': self.build_script,
			'run_script' : self.run_script,
			'correct_output' : self.correct_output,
			'timeout_warn' : self.timeout_warn,
			'timeout_stop' : self.timeout_stop
		}
		return json.dumps(data, indent=4, sort_keys=True)


	def validateOutput(self, program_output):
		tmp_file_name = "tmp/"+self.test_name+".out"
		f = open(tmp_file_name, 'w')
		f.write(program_output)
		f.close()
		if (self.correct_output != ""):
			if os.path.isfile(self.correct_output):
				diff = "diff " + self.correct_output + " " + tmp_file_name
				command = Cmd(diff,60)
				if command.output:
					return False
				else:
					return True

	def compile(self):
		Cmd(self.build_script, 60)
		# add checks for compilation

	def run(self):
		command = Cmd(self.run_script, self.timeout_stop)
		output_correct = self.validateOutput(command.output)
		data =  self.test_name, str(command.runtime) , str(output_correct) ,str(command.returncode == -11), str(command.returncode == -15)
		string = ""
		for word in data:
			col_width = 20
			string = string + "".join(word.ljust(col_width) )
		print(string)



if __name__ == "__main__":
	testplan_file = "testplan.plan"
	if (len(sys.argv) > 1):
		testplan_file = sys.argv[1]
	if (os.path.isfile(testplan_file) == False):
		print("create testplan.plan plan file")
		sys.exit()
	f = open(testplan_file, 'r')
	p = Testplan("temp name")
	p.decodeJson(f.read())
	data =  "NAME", "RUNTIME" , "OUTPUT_CORRENT" , "SEGFAULT", "TIMEOUT"
	string = ""
	for word in data:
		col_width = 20
		string = string + "".join(word.ljust(col_width) )
	print string
	p.executePlan()

