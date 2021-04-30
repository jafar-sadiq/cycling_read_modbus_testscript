import csv,math,sys,subprocess

fix_reg_values=['0x10','0x30','0x38','0x40']
var_reg_values=['0x8c','0x8a','0x96']
var_reg_range={'0x8a':(12,13),'0x8c':(10,265),'0x96':(30,3300)}

#function to check fix type registers
def fix_reg_func(expected,actual,host=None):
    if expected==actual:
        return True
    else:
        print(f"{actual} doesn't match with first time read_data value")
        return False

#function to check variable type registers
def var_reg_func(out,min,max,host=None):
    values_list=list(out.split(','))[2:]
    values_list=[math.ceil(float(i)) for i in values_list]
    for value in values_list:
        if value<=min or value>=max:
            print(f"{value} is out of range")
            return False
        return True


#driver code
#cmd args
#file.py reg_type reg_value host obb min max new_reg_type new_reg_value

args=sys.argv

reg_type=sys.argv[1]
reg_value=sys.argv[2]
host=sys.argv[3]
obb=sys.argv[4]
min=sys.argv[5] 
max=sys.argv[6]
new_reg_type=sys.argv[7]
new_reg_value=sys.argv[8]


if new_reg_type!=None and new_reg_value not in fix_reg_values and new_reg_value not in var_reg_values:
    if new_reg_type=='fix':
        fix_reg_values.append(new_reg_value)
    elif new_reg_type=='variable':
        var_reg_values.append(new_reg_value)

myfile=open('output.csv','w')
writer=csv.writer(myfile)
writer.writerow('Register Type','Register Value','Expected','Error')

i=0
while i<1000:
    cmd=subprocess.Popen(f"orv2_query --output=csv --register 0x10 {host}",shell=True)
    out=str(cmd.communicate())

    #if reg_value is fix type
    if reg_value in fix_reg_values:
        if i==0:
            expected=out
            continue
        actual=out
        if not fix_reg_func(expected,actual,reg_value):
            #write to csv file
            writer.writerow('fix',reg_value,actual,out)
            break

    #if reg_value is variable type
    elif reg_value in var_reg_values:
        min,max=var_reg_range[reg_value]
        if not var_reg_func(out,min,max):
            #write to csv file
            writer.writerow('variable',reg_value,'NA',out)
            break

    i+=1

myfile.close()