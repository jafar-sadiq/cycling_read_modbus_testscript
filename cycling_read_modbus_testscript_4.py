import csv,math,sys,subprocess,argparse

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
#file.py reg_type reg_value host obb no_of_times min max new_reg_type new_reg_value

parser=argparse.ArgumentParser()

parser.add_argument('reg_type')
parser.add_argument('reg_value')
parser.add_argument('host')
parser.add_argument('obb')
parser.add_argument('no_of_times',type=int)
parser.add_argument('min',default=None)
parser.add_argument('max',default=None)
parser.add_argument('new_reg_type',default=None)
parser.add_argument('new_reg_value',default=None)

args=parser.parse_args()


if args.new_reg_type!=None and args.new_reg_value not in fix_reg_values and args.new_reg_value not in var_reg_values:
    if args.new_reg_type=='fix':
        fix_reg_values.append(args.new_reg_value)
    elif args.new_reg_type=='variable':
        var_reg_values.append(args.new_reg_value)

myfile=open('output.csv','w')
writer=csv.writer(myfile)
writer.writerow('Register Type','Register Value','Expected','Error')

i=0
while i<args.no_of_times:
    cmd=subprocess.Popen(f"orv2_query --output=csv --register 0x10 {args.host}",shell=True)
    out=str(cmd.communicate())

    #if reg_value is fix type
    if args.reg_value in fix_reg_values:
        if i==0:
            expected=out
            continue
        actual=out
        if not fix_reg_func(expected,actual,args.reg_value):
            #write to csv file
            writer.writerow('fix',args.reg_value,actual,out)
            break

    #if reg_value is variable type
    elif args.reg_value in var_reg_values:
        min,max=var_reg_range[args.reg_value]
        if not var_reg_func(out,min,max):
            #write to csv file
            writer.writerow('variable',args.reg_value,'NA',out)
            break

    i+=1

myfile.close()