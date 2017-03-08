import os

INPUT_PATH = os.path.join(os.path.abspath(os.pardir),'INPUTS')
ELEC_FILE_NAME = 'elec_demand_DA_2014.csv'
ELEC_FILE = os.path.join(INPUT_PATH,ELEC_FILE_NAME)
DIST_FILE_NAME = 'DA_dist_matrix.csv'
DIST_FILE = os.path.join(INPUT_PATH,DIST_FILE_NAME)

GEN_DICT = {'c':3942000,'ng':1752000,'n':10950000,'b':10950,'h':525600,'sw':87.6,'lw':2190000,'ss':87.6,'ls':525600}

genList = ['c','ng','n','b','h','sw','lw','ss','ls']