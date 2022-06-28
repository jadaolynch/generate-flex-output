#!/usr/bin/python3
#       MULTIPLE_OUTPUTS.PY
#       author : Jada Olivia lynch (June 2022)
#
#       for running flexpart with multiple releases
#       and returning output for each run, without overlap
#
#       * required input
#       inputs :
#           * met_dir   (str) : directory for wind fields
#           * data_dir  (str) : directory to csv containing names, dates etc.
#                               (see README for proper format)
#           options_dir (str) : directory to options folder
#           output_dir  (str) : directory for model output
#           scr_dir     (str) : directory to the FLEXPART src
#           avail_dir   (str) : directory for AVAILABLE file
#
#       execute from main FLEXPART directory (example : ~/FLEXPART)
#
#       requirements : Python 3.9 (at least), os, pandas, time
#

import os
import time

import pandas as pd

# * USER INPUT:
data_dir = ""
met_dir = ""

# OPTIONAL : change only if your output directory isnt its default directory/directory has different name

output_dir = ""
options_dir = ""
src_dir = ""
avail_dir = ""

# AFTER THIS USER DOES NOT HAVE TO CHANGE ANYTHING

# adjust user input
dir_dict = {
    "options/" : str(options_dir),
    "output/" : str(output_dir),
    "src/" : str(src_dir),
    "AVAILABLE" : str(avail_dir)
}

# get current working directory
cwd = os.getcwd() + "/"
for key in dir_dict.keys():
    if dir_dict[key] == "":
        dir_dict[key] = cwd + key
    else:
        if key == "AVAILABLE":
            continue
        elif dir_dict[key][len(dir_dict[key])-1] != "/":
            dir_dict[key] += "/"
            corrected = "added '/' to {dir}"
            print(corrected.format(dir = (dir_dict[key])))

# read input data
df = pd.read_csv(data_dir)

class Run:

    def __init__(self) -> None:
        self.comments = df.iloc[:,0]
        self.range = len(self.comments)
        self.start_dates = df.iloc[:,1]
        self.start_times = df.iloc[:,2]
        self.stop_dates = df.iloc[:,3]
        self.stop_times = df.iloc[:,4]
        pass

    def _run_FLEXPART(self)  -> None:
        """executes FLEXPART in src"""
        src_dir = dir_dict["src/"]
        execute = "{src}FLEXPART"
        os.system(execute.format(src = src_dir))
        pass

    def _check_time(time) -> None:
        if time == 0:
            time = "000000"
        return str(time)

    def _write_to_RELEASES(self, i) -> None:
        """changes input dates/times in RELEASES file"""
        options = dir_dict["options/"]
        RELEASES_dir = options + "RELEASES"
        old_RELEASES = options + "RELEASES_og"
        copy_RELEASES = "cd {options} && mv RELEASES RELEASES_og"
        os.system(copy_RELEASES.format(options = options))
        with open(old_RELEASES, "r+") as RELEASES_og:
            RELEASES_lines = RELEASES_og.readlines()
            header = RELEASES_lines[0:15]; remainder = RELEASES_lines[19:]
        start_time = Run._check_time(self.start_times[i])
        stop_time = Run._check_time(self.stop_times[i])
        new_dates = [" IDATE1  =        " + str(self.start_dates[i]) + ",\n", " ITIME1  =        " + str(start_time) + ",\n",
                     " IDATE2  =        " + str(self.stop_dates[i]) + ",\n", " ITIME2  =        " + str(stop_time) + ",\n"]
        header = "".join(header); new_dates = "".join(new_dates); remainder = "".join(remainder)
        with open(RELEASES_dir, "a+") as RELEASES:
            RELEASES.write(header)
            RELEASES.write(new_dates)
            RELEASES.write(remainder)
        pass

    def _write_to_COMMAND(self, i) -> None:
        """writes input dates/times to COMMAND """
        options = dir_dict["options/"]
        COMMAND_dir = options + "COMMAND"
        old_COMMAND = options + "COMMAND_og"
        copy_COMMAND = "cd {options} && mv COMMAND COMMAND_og"
        os.system(copy_COMMAND.format(options = options))
        with open(old_COMMAND, "r") as old_COMMAND:
            cmd_lines = old_COMMAND.readlines()
            header = cmd_lines[0:8]
            remainder = cmd_lines[12:]
        start_time = Run._check_time(self.start_times[i])
        stop_time = Run._check_time(self.stop_times[i])
        new_lines = [ " IBDATE=         " + str(self.start_dates[i]) + ",\n", " IBTIME=           " + start_time + ",\n",
                     " IEDATE=         " + str(self.stop_dates[i]) + ",\n", " IETIME=           " + stop_time + ",\n"]
        header = "".join(header); new_lines = "".join(new_lines); remainder = "".join(remainder)
        with open(COMMAND_dir, "a+") as COMMAND:
            COMMAND.write(header)
            COMMAND.write(new_lines)
            COMMAND.write(remainder)
        pass

    def _change_pathnames(self) -> None:
        """writes to pathnames and changes pathnames. Can easily
           be modified to account for multiple output directories"""
        pathnames_dir = "pathnames"
        os.system("rm pathnames")
        with open(pathnames_dir, "a+") as PATHNAMES:
            PATHNAMES.write(dir_dict["options/"] + "\n")
            PATHNAMES.write(dir_dict["output/"] + "\n")
            PATHNAMES.write(met_dir + "\n")
            PATHNAMES.write(dir_dict["AVAILABLE"] + "\n")
        pass

    def run(self) -> None:
        """main method, writes to RELEASES, COMMAND (and sometimes pathnames), and
           executes FLEXPART"""
        prepare = "Preparing run no. {index}"
        running = "Running run no. {index}"
        for i in range(1, self.range + 1):
            print(prepare.format(index = i))
            self._write_to_RELEASES(i)
            self._write_to_COMMAND(i); #self._change_pathnames()
            print(running.format(index = i))
            self._run_FLEXPART()
            time.sleep(2)
        print("Done!")
        pass

if __name__ == "__main__":

    object = Run()
    object.run()

#    object._write_to_RELEASES(1)
#    object._write_to_COMMAND(1)
#    object._change_pathnames()
    
