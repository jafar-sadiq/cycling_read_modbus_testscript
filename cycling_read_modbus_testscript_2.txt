import csv,math

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
myfile=open('output.csv','w')
writer=csv.writer(myfile)
writer.writerow('Register Type','Register Value','Expected','Error')

i=0
while i<1000:
    out=...
    reg_value=list(out.split(','))[0]

    #if reg_value is fix type
    if reg_value in fix_reg_values:
        if i==0:
            expected=out
            continue
        actual=out
        if not fix_reg_func(expected,actual,reg_value):
            #write to csv file
            writer.writerow('fix',reg_value,out)
            break

    #if reg_value is variable type
    elif reg_value in var_reg_values:
        min,max=var_reg_range[reg_value]
        if not var_reg_func(out,min,max):
            #write to csv file
            writer.writerow('variable',reg_value,out)
            break

    i+=1

myfile.close()