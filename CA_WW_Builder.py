import subprocess
import os
import re
import datetime
import openpyxl
import sys

##################### bloop ###############################################

try:
  UR_XL_Start_Row = int(sys.argv[1])
  UR_XL_End_Row = int(sys.argv[2])
except IndexError:
  UR_XL_Start_Row = 3
  UR_XL_End_Row = 30


####################################################################
###  D E F I N E   F I L E S
# file_dir = "/mnt/hgfs/Circle_Of_Blue/Brett_Walton/"
file_dir = "./"

file_BASE_HTML = file_dir + "California_Waste_Water_BASE.html"

#file_beg = file_dir + "California_Waste_Water_START.txt"
#file_info_window = file_dir + "California_Waste_Water_INFO_WIN.txt"
#file_middle = file_dir + "California_Waste_Water_MIDDLE_01.txt"
#file_end = file_dir + "California_Waste_Water_END.txt"

file_target_html = file_dir + "California_Waste_Water_TARGET.html"

file_sorted_data_in = file_dir + "XL_Good_SORTED_Rows_Out.txt"

####################################################################



absolutely_unused_variable = os.system("clear")

print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'\n\n')

####################################################################
####################################################################
####################################################################
#
#   S U B R O U T I N E S
#
#def concatenate_html():
#  print ("trying to build HTML file")
#  rc = os.system("cat " + file_beg + " " + file_middle + " " + file_end + " > " + file_html)
#  print("Here rc = ", rc)
#
#  return;


def comma(num):
    '''Add comma to every 3rd digit. Takes int or float and
    returns string.'''
    if type(num) == int:
        return '{:,}'.format(num)
    elif type(num) == float:
        return '{:,.2f}'.format(num) # Rounds to 2 decimal places
    else:
        print("Need int or float as input to function comma()!")

#  interpolate color value
def iGetColor(x, low, low_color, high, high_color):
    #BREAK low_color into rr,gg,bb as HEX, and interpolate THOSE with high_color RR,GG,BB

    hexcolor_LO = hex(low_color)
    rr = int( hexcolor_LO[2:4], 16 )
    gg = int( hexcolor_LO[4:6], 16 )
    bb = int( hexcolor_LO[6: ], 16 )

    hexcolor_HI = hex(high_color)
    RR = int( hexcolor_HI[2:4], 16 )
    GG = int( hexcolor_HI[4:6], 16 )
    BB = int( hexcolor_HI[6: ], 16 )

#    input( "i/p digit")

    vRed   =  int(   (  (high - x) * rr  +  (x - low) * RR  ) / (high - low)   )
    vGreen =  int(   (  (high - x) * gg  +  (x - low) * GG  ) / (high - low)   )
    vBlue  =  int(   (  (high - x) * bb  +  (x - low) * BB  ) / (high - low)   )

    iVal = vRed * 65536 + vGreen * 256 + vBlue

#    print( rr, gg, bb, RR, GG, BB, low, high, x, "  v= ", v )
#    input("digit please   ")

    return iVal;

####################################################################
####################################################################
####################################################################


with open(file_BASE_HTML,'r') as f:
#  fiw_data = "Holy Name \n"
	f_data = f.read()
#	f_intro = f_data


iEnd_0 = f_data.find("///////////////////////////   BASE_POINT_START   ////////////////////////////////////")
iEnd_1 = f_data.find("///////////////////////////   BASE_POINT_END   //////////////////////////////////////")
iEnd_2 = f_data.find("///// INSERT_NEXT_PIN_HERE /////")

BegPartHTML = f_data[0:iEnd_0]
BasePointMarker_HTML = f_data[iEnd_0:iEnd_2]
bpm = BasePointMarker_HTML
EndPartHTML = f_data[iEnd_2:]

if 0 == 1:
  print("BegPartHTML >>>>>>>>  \n")
  print( BegPartHTML)

  print("BasePointMarker_HTML >>>>>>>>  \n")
  print( BasePointMarker_HTML)

  print("EndPart_HTML >>>>>>>>  \n")
  print( EndPartHTML)


f.close

# SEE IF NUMBER IS LISTED

Lat_MAX = -10000
Lat_MIN =  10000

Long_MAX = -10000
Long_MIN =  10000

f_sorted_IN = open(file_sorted_data_in,'r')



# waste water fee levels
level0 = 0
level1 = 25
level2 = 40
level3 = 100
level4 = 188

# pin colors
iCLR_0  = int('0xFFFFFF',16)   #  level0
iCLR_1  = int('0xFFFF00',16)   #  level1
iCLR_2  = int('0xFF8500',16)   #  level2
iCLR_3  = int('0xFF0000',16)   #  level3
iCLR_4  = int('0xFF00FF',16)   #  level4





with open(file_target_html,'w') as f_out:

  #input("Clown Boy "  )
  #exit()

  data_pin_list_OUT = ""

  counter = -1
  for currentline in f_sorted_IN:
    counter += 1
#    if counter == 10:
#      break     #  exit()

    wk1 = currentline[:-1]   # remove rightmost trailing ";"

    print(counter, "   wk1 =  ", wk1)

    workline = wk1.split(";")   # split up and place into array
#    nn = len(workline)
#    for zz in range(0, nn):
#      print(  workline[zz].strip()  )
#      input("zz = " + str(zz) + "   ENTER DIGIT     ")

    agency_cob_PY = workline[1]
    city_town_cob_PY = workline[2]
    zipcode_cob_PY = workline[3]
    latitude_cob_PY = float(workline[7])
    longitude_cob_PY = float(workline[9])

#    input("A counter = " + str(counter) + "    Enter digit: " )

    try:
      Population_cob_PY = comma(int(workline[10]))
    except TypeError:
      Population_cob_PY = "N/A"

#    input("B counter = " + str(counter) + "    Enter digit: " )


    MedianHouseholdIncome_cob_PY = int(workline[11])
    if MedianHouseholdIncome_cob_PY == 0:
      MedianHouseholdIncome_cob_PY = "N/A"
    else:
      MedianHouseholdIncome_cob_PY = comma(MedianHouseholdIncome_cob_PY)

    WasteWaterUserFee_cob_PY = int( float( workline[12] ) + 0.50 )

#    input("C counter = " + str(counter) + "    Enter digit: " )

    if latitude_cob_PY > Lat_MAX:
      Lat_MAX = latitude_cob_PY
    if latitude_cob_PY < Lat_MIN:
      Lat_MIN = latitude_cob_PY

    if longitude_cob_PY > Long_MAX:
      Long_MAX = longitude_cob_PY
    if longitude_cob_PY < Long_MIN:
      Long_MIN = longitude_cob_PY


#  fill in Base Point Marker with new pin data
    bpm1 = bpm
    bpm2 = bpm1.replace("AGENCY_XXX", str(agency_cob_PY))
    bpm3 = bpm2.replace("CITY_TOWN_XXX", str(city_town_cob_PY))
    bpm35 = bpm3.replace("ZIP_XXX", str(zipcode_cob_PY))
    bpm4 = bpm35.replace("MEDIAN_HOUSEHOLD_INCOME_XXX", str(MedianHouseholdIncome_cob_PY))
    bpm5 = bpm4.replace("WASTEWATER_USER_FEE_XXX", comma(WasteWaterUserFee_cob_PY))
    bpm6 = bpm5.replace("POPULATION_XXX", str(Population_cob_PY))
    bpm7 = bpm6.replace("sContentXXX","sContent" + str(counter))
    bpm8 = bpm7.replace("markerXXX","marker" + str(counter))
    bpm9 = bpm8.replace("Lat_XXX",str(latitude_cob_PY))
    bpm10 = bpm9.replace("Long_XXX",str(longitude_cob_PY))
    bpm11 = bpm10.replace("MarkerTitleXXX", str(agency_cob_PY))
    bpm_data_mod = bpm11

#    print(">>>>>>>  bpm_data_mod >>> /n")

#    print(bpm_data_mod)

#    input("chumpy " + str(wk1) )
#    exit()


# color code pin based on Waste Water Fee
    if (WasteWaterUserFee_cob_PY > 0):
      wk1 = WasteWaterUserFee_cob_PY

      if wk1 <= level1:
        iColor = iGetColor(wk1, level0, iCLR_0, level1, iCLR_1)

      elif wk1 <= level2:
        iColor = iGetColor(wk1, level1, iCLR_1, level2, iCLR_2)

      elif wk1 <= level3:
        iColor = iGetColor(wk1, level2, iCLR_2, level3, iCLR_3)

      elif wk1 <= level4:
        iColor = iGetColor(wk1, level3, iCLR_3, level4, iCLR_4)

      else:
        input("you've got a bad range setup. wk1 = " + str(wk1) + "  enter DIGIT : ")
        exit()


      hexColor =  hex(iColor)[2: ]



      data_pin_list_OUT += bpm_data_mod.replace("HEXCOLORXXX", hexColor) + '\n'

#      name1 = input("Input digit")

### OUTSIDE FOR LOOP, Calculate Center of map
  Lat_Center = str((float(Lat_MAX) + float(Lat_MIN)) / 2)
  Long_Center = str((float(Long_MAX) + float(Long_MIN)) / 2)

  BegPartHTML_mod = BegPartHTML.replace('LAT_CENTER_XXX', Lat_Center).replace('LONG_CENTER_XXX', Long_Center)
#  BegPartHTML_mod = BegPartHTML.replace(LAT_CENTER_XXX, Lat_Center)

  BegPartHTML_mod = BegPartHTML_mod.replace("level_0_CHARGE_XXX", str(level0))
  BegPartHTML_mod = BegPartHTML_mod.replace("level_1_CHARGE_XXX", str(level1))
  BegPartHTML_mod = BegPartHTML_mod.replace("level_2_CHARGE_XXX", str(level2))
  BegPartHTML_mod = BegPartHTML_mod.replace("level_3_CHARGE_XXX", str(level3))
  BegPartHTML_mod = BegPartHTML_mod.replace("level_4_CHARGE_XXX", str(level4))
  BegPartHTML_mod = BegPartHTML_mod.replace("XXX_CLR_0_XXX", hex(iCLR_0)[2:])
  BegPartHTML_mod = BegPartHTML_mod.replace("XXX_CLR_1_XXX", hex(iCLR_1)[2:])
  BegPartHTML_mod = BegPartHTML_mod.replace("XXX_CLR_2_XXX", hex(iCLR_2)[2:])
  BegPartHTML_mod = BegPartHTML_mod.replace("XXX_CLR_3_XXX", hex(iCLR_3)[2:])
  BegPartHTML_mod = BegPartHTML_mod.replace("XXX_CLR_4_XXX", hex(iCLR_4)[2:])



  total_out_HTML = BegPartHTML_mod + data_pin_list_OUT + EndPartHTML
  f_out.write(total_out_HTML)

f_out.close


exit()

##################################################################################
