from __future__ import print_function

from operator import itemgetter, attrgetter

import requests
import subprocess
import os
import re
import datetime
import openpyxl
import sys
import math
import time


####################################################################

try:
  UR_XL_Start_Row = int(sys.argv[1])
  UR_XL_End_Row = int(sys.argv[2])
except IndexError:
  UR_XL_Start_Row = 26
  UR_XL_End_Row = 30


####################################################################
###  D E F I N E   F I L E S 
file_dir = "/mnt/hgfs/Circle_Of_Blue/Brett_Walton/"

PYTHON_WK_DIR = "/home/tcr/Desktop/python_work/"
XL_Bad_Rows_Out = open("XL_Bad_Rows_Out.txt", "w")
XL_Good_Rows_Out = open("XL_Good_Rows_Out.txt", "w")
Good_SORTED_PRE_ADJ = open("Good_SORTED_PreAdjust.txt", "w")
XL_Good_SORTED_Rows_Out = open("XL_Good_SORTED_Rows_Out.txt", "w")

file_XL = file_dir + "TCR_California_fy1617ww_user_charge_survey.xlsx"
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
####################################################################

from openpyxl import Workbook
XL_doc = openpyxl.load_workbook(file_XL)
sheet = XL_doc.get_sheet_by_name('Sheet2')
#sheet = XL_doc.get_sheet_by_name('Survey Data (By Agency)')

###############      C L A S S    ################################

class CoordVal(object):
  def __init__(self, y0, y1):
     self.lat = y0
     self.long = y1



####################################################################
###  C L A S S E S

#XL_row = [[]] * 9  #define XL_row as list

class XL_row(object):
  def __init__ (self, orow, oagency, ocity, ozipcode, ooccurence, ototal_occur, olatitude, onewlat, olongitude, onewlong, opopulation, oincome, owwfee):
    self.row = orow
    self.agency = oagency
    self.city = ocity
    self.zipcode = ozipcode
    self.occurence = ooccurence
    self.total_occur = ototal_occur
    self.latitude = olatitude
    self.newlat = onewlat
    self.longitude = olongitude
    self.newlong = onewlong
    self.population = opopulation
    self.income = oincome
    self.fee = owwfee
    
  def __repr__(self):
    return "<row: %s, agency: %s, lat: %s, long: %s >" % (self.row, self.agency, self.latitude, self.longitude)

  def __str__(self):
    return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.row, self.agency, self.city, self.zipcode, self.occurence, self.total_occur, self.latitude, self.newlat, self.longitude, self.newlong, self.population, self.income, self.fee)
  

#---------------------------------------------------------

    

##########################################################################
###  D E F I N E    L I S T S

#define XL_all_rows as list (a list of   XL_row   objects)  Use dummy first so attributes available
XL_all_rows = [XL_row(-1, "dummy_agency", "dummy_city", "dummy_zipcode", "dummy_occurence", "dummy_total_occur", "dummy_latitude", "dummy_newlat", "dummy_longitude", "dummy_newlong", "dummy_population", "dummy_income", "dummy_wwfee")] 

# Now remove dummy ( ok since list type established )
XL_all_rows.pop()
  

  
  
###############   F U N C T I O N ################################

    
# READ TRAVEL SITE
def getLatLong(sCityIn):

  print(sCityIn)

  time.sleep(3)
  
  TRAVEL_site = "http://www.travelmath.com/cities/" + sCityIn + ",+CA"
  response = requests.get(TRAVEL_site).text  
  
  iBeg = response.find("<h3")   # get to start of lat & long box
  iEnd = response.find("</h3>")

  jLo = len('<h3 class=\"space\">')
  mystring = response[iBeg+jLo:iEnd]

  mystring = mystring.replace('<h3 class=\"space\">','')
  mystring = mystring.replace('<span class="slash">/</span>','')
  mystring = mystring.replace('&deg;','')
  mystring = mystring.replace('"','')
  mystring = mystring.replace("'","")

  coord = mystring.split()
#  for i in range(0, len(coord)):
#    print (coord[i])

  fLat = float(coord[0]) + float(coord[1]) / 60 + float(coord[2]) / 3600
  if coord[3] == 'S':
    fLat *= -1

  fLong = float(coord[4]) + float(coord[5]) / 60 + float(coord[6]) / 3600
  if coord[7] == 'W':
    fLong *= -1

  #  print(fLat, fLong, '\n\n')

  #  input( "mystring  " + mystring  + "   Enter Digit:  ")
  
  return CoordVal( fLat, fLong );


####################################################################

  
##########################################################################
###  S U B R O U T I N E S

def ret_cell_value(col, irow, rettype):
	val_in = repr(sheet[col + str(irow)].value)   ##  converts cell to return printable !!
	
	
	if rettype == 'int':
		if val_in == 'None':
			val_out = '0'
		else:
			val_out = val_in.rstrip('L')  ##  note that floats that are coming in from XL are unicode converted as integers, so ALWAYS STRIP 'L' if there is one
	if rettype == 'float':
		if val_in == 'None':
			val_out = '0'
		else:
			if 'L' in val_in:
				val_out = val_in.rstrip('L')  ##  note that floats that are coming in from XL are unicode converted as integers, so ALWAYS STRIP 'L' if there is one
			else:
				val_out = str(val_in)		
	if rettype == 'str':
		if val_in == 'None':
			val_out = "N/A"
		else:
			val_out = val_in.lstrip("u'").rstrip("'")  # to convert UNICODE string to just plain str
	return val_out;


#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#######################################################################


#absolutely_unused_variable = os.system("clear")

#print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\n\n')
## XL_Text_Out = open(PYTHON_WK_DIR + list_out, "w")


# row_num, agency, city, zip, lat, long, pop, income, wwfee
ROW_NUM = 0
AGENCY = 1
CITY = 2
ZIP = 3
LAT = 4
LNG = 5
POPUL = 6
INCOME = 7
WWFEE = 8


  

for n in range( UR_XL_Start_Row, UR_XL_End_Row ):
  row_num = n
  agency = ret_cell_value('A',n,'str')
  city = ret_cell_value('C',n,'str')
  zipcode = ret_cell_value('D',n,'int')
  occurence = -1									# keeps track of how often SAME LAT & LONG occur in dataset
  total_occur = -1									# keeps track of how often SAME LAT & LONG occur in dataset
  latitude  = ret_cell_value('F',n,'float')[:7]
  newlat = 100
  longitude = ret_cell_value('G',n,'float')[:9]
  newlong = 10000
  population = ret_cell_value('J',n,'int')
  income = ret_cell_value('K',n,'int')
  wwfee = ret_cell_value('O',n,'float')
  
##  TCR inject new lat/long  
  newCoord = getLatLong( city )
  latitude = str(newCoord.lat)[:7]
  longitude = str(newCoord.long)[:9]
##


  t_obj = XL_row(row_num, agency, city, zipcode, occurence, total_occur, latitude, newlat, longitude, newlong, population, income, wwfee)

  
  print("ajfoyt Row ", str(t_obj.row), agency[:15], str(t_obj.zipcode), "  occurence ", str(t_obj.occurence), "  total_occur ", str(t_obj.total_occur), "  lat = ", t_obj.latitude, "  newlat = ", t_obj.newlat, "  long = ", t_obj.longitude, "  newlong = ", t_obj.newlong )
#  if t_obj.fee == 0:
#    print( t_obj.row, t_obj.agency, t_obj.fee, file = XL_Bad_Rows_Out )
#  else:	
#    print( t_obj.row, t_obj.agency, t_obj.fee, file = XL_Good_Rows_Out )
    
  XL_all_rows.append(t_obj)
    
    
##----------------------------------
#XL_SORTED_ROWS_BY_LAT_LNG = XL_all_rows  

sorted_lat_long =  sorted(XL_all_rows, key = attrgetter('latitude','longitude'))

print( "XXXXXXXXXX SORTED BY LAT LONG  XXXXXXXXXXXXXXXXXXXX")

for i in range ( 0, len(sorted_lat_long)):
  s1 =  sorted_lat_long[i].agency[:15]
  s2 =  sorted_lat_long[i].zipcode
  s3 =  sorted_lat_long[i].latitude
  s4 =  sorted_lat_long[i].longitude
  print( s1 , s2, s3, s4 , file = Good_SORTED_PRE_ADJ)  

print( "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

###############   C L A S S ################################

class CoordVal(object):
  def __init__(self, y0, y1):
     self.lat = y0
     self.long = y1
     





# FUNCTION  FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
def calc_newlat(olatitude, olongitude, ototal_number_of_arcs, othis_arc_number):
	arc_inc = 2 * math.pi / ototal_number_of_arcs 
	radius = 0.05
	arc = othis_arc_number * arc_inc

	lat_adjust = math.sin(arc) * radius
	lat_back = str(float(olatitude) + lat_adjust)

	long_adjust = math.cos(arc) * radius
	long_back = str(float(olongitude) + long_adjust)

	return CoordVal( lat_back, long_back ); 




#  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

#cluster = []   # list of rows of those agencies with same lat & long

imax = len(sorted_lat_long)

for i in range(0, imax):

  old_lat = sorted_lat_long[i-1].latitude
  old_lng = sorted_lat_long[i-1].longitude
  old_occurence = sorted_lat_long[i-1].occurence

  new_lat = sorted_lat_long[i].latitude
  new_lng = sorted_lat_long[i].longitude

  if ( new_lat == old_lat ) and ( new_lng == old_lng ) :
    back_idx = sorted_lat_long[i - 1].occurence + 1
    for jj in range(0, back_idx):
      sorted_lat_long[i - jj].total_occur = back_idx
      sorted_lat_long[i - jj].occurence   = back_idx - jj
  else :
    sorted_lat_long[i].occurence   = 1
    sorted_lat_long[i].total_occur = 1
      
print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    
	
	
	
for kk in range ( 0, len(sorted_lat_long)):
#	if sorted_lat_long[i].fee != 0:
	
	if sorted_lat_long[kk].total_occur == 1:
		sorted_lat_long[kk].newlat  = sorted_lat_long[kk].latitude
		sorted_lat_long[kk].newlong = sorted_lat_long[kk].longitude
	else:
		ccc = calc_newlat( sorted_lat_long[kk].latitude, sorted_lat_long[kk].longitude, sorted_lat_long[kk].total_occur, sorted_lat_long[kk].occurence)
		sorted_lat_long[kk].newlat =  ccc.lat
		sorted_lat_long[kk].newlong = ccc.long

	s0 =  sorted_lat_long[kk].row
	s1 =  sorted_lat_long[kk].agency
	s2 =  sorted_lat_long[kk].city
	s3 =  sorted_lat_long[kk].zipcode
	s4 =  sorted_lat_long[kk].occurence
	s5 =  sorted_lat_long[kk].total_occur
	s6 =  sorted_lat_long[kk].latitude
	s7 =  sorted_lat_long[kk].newlat
	s8 =  sorted_lat_long[kk].longitude
	s9 =  sorted_lat_long[kk].newlong
	sA =  sorted_lat_long[kk].population
	sB =  sorted_lat_long[kk].income
	sC =  sorted_lat_long[kk].fee
	
	
	print( s0, s1[:15] , s2[:12], s3, s4, s5, s6, s7, s8, s9 )  #, file = XL_Good_SORTED_Rows_Out)  
	print( s0, "; ", s1, "; ", s2, "; ", s3, "; ", s4, "; ", s5, "; ", s6, "; ", s7, "; ", s8, "; ", s9, "; ", sA, "; ", sB, "; ", sC, "; ", file = XL_Good_SORTED_Rows_Out)  

#    self.row = orow
#    self.agency = oagency
#    self.city = ocity
#    self.zipcode = ozipcode
#    self.occurence = ooccurence
#    self.total_occur = ototal_occur
#    self.latitude = olatitude
#    self.newlat = onewlat
#    self.longitude = olongitude
#    self.newlong = onewlong
#    self.population = opopulation
#    self.income = oincome
#    self.fee = owwfee
	
      
      
exit()

####################################################################
####################################################################
####################################################################
