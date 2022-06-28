# Run FLEXPART and get seperate output files for each run

### This small script allows users to get seperate output files when running multiple FLEXPART runs. 

## Content : 
### 1. multiple_output.py
   Python 3 script to prepare the model and run it.
   
### 2. example_input_data.csv
   Comma seperated dataset given as an example of how the script uses the inputs to prepare the model.
   
## How it works : 
#### 1. Clone repository to FLEXPART home directory

      example : /home/<user>/FLEXPART/

#### 2. User provides proper input data that is comparable to those given in example_input_data.csv
#### 3. User provides directories required in multiple_outputs.py
#### 4. Run:

      $ python3 multiple_outputs.py
      
      *you may have to use sudo*
      
#### 5. Find output files in the provided output directory

## Requirements
1. Python3.9
2. Pandas 

## Testing
Tested on Ubuntu 20.04, Python 3.10.5
