def cleanNumber(string_number):
    
    if not isinstance(string_number, str):
        raise TypeError("The 'string_number'argument must be a string!")

    lst = []
    for char in string_number:
        if char != ',':
            lst.append(char)
    num = int(''.join(lst))
    return num

def cleanDate(string_date):

    if not isinstance(string_date, str):
        raise TypeError("The 'string_date' argument must be string")

    try:
        lst = string_date.split()
        month = lst[1]
        new_month = None
        match month:
            case 'Jan':
                new_month = '01'
            case 'Feb':
                new_month = '02'
            case 'May':
                new_month = '03'
            case 'April' | 'Ap' | 'Apr':
                new_month = '04'
            case 'March' | 'Mar':
                new_month = '05'
            case 'Jun':
                new_month = '06'
            case 'July' | 'Jul':
                new_month = '07'
            case 'Aug':
                new_month = '08'
            case 'Sep':
                new_month = '09'
            case 'Oct':
                new_month = '10'
            case 'Nov':
                new_month = '11'
            case 'Dec':
                new_month = '12'
        
        new_date = lst[2] + '-' + new_month + '-' + lst[0]
        return new_date
    except:
        return '1850-10-10'

if __name__ == '__main__':
    print(cleanDate('01 April 2012'))