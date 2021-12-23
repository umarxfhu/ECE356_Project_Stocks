import mysql.connector
from mysql.connector import Error
import pandas as pd
import datetime

class ClientApp:
    def __init__(self):
        self.name = "stonkapp"
        self.prefix = "[mainmenu] "
        self.connection = "e"
    
    def mainmenu(self):    
        pw = "Rgb_356$" # IMPORTANT! Put your MySQL Terminal password here.
        db = "db356_rvictork" # This is the name of the database we will create in the next step - call it whatever you like.

        self.connection = create_db_connection("marmoset04.shoshin.uwaterloo.ca","rvictork", pw, db)

        while(True):    
            self.prefix = "[main menu] "
            print()
            print("====================== Main menu ====================================")
            choiceList = """
                1. Look up record
                2. Update existing records
                3. Add new record
                4. Delete record
                5. Quit
                """
            print(choiceList)
            choice = input(self.prefix + "Enter selection number: ")
            
            if (choice == "1"):
                self.lookup()
            elif (choice == "2"):
                self.update()
            elif (choice == "3"):
                self.insert()
            elif (choice == "4"):
                self.delete()
            elif (choice == "5"):

                print("\nBye!!!")
                break
            else:
                input("Invalid input. Press any key to continue...")
          

        self.connection.close()
        print("\n[INFO]: Connection to DB server closed.")
            
                
            
    def lookup(self):
        self.prefix = "[lookup mode] "
        print()
        print("--------------------- Lookup Mode ---------------------")
        choiceList = """
            About companies:
            1. Lookup company information
            2. Lookup company yearly performance data
            
            About stocks:
            3. Lookup stock daily data
            4. Lookup specific stock's latest data
            
            Other:
            5. Find articles
            6. View comments
            """
        print(choiceList)
        choice = input(self.prefix + "Enter selection number: ")
        
        line = "-------"
        if (choice == "1"):
            print(line + "Lookup company information"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            query = "select * from Company where symbol = %s"
            result = read_query(self.connection, query, [symbol])
            self.displayCompanyData(result)
            result = read_query(self.connection, "select name as 'CEO name', age as 'CEO age' from CEO inner join CEOruns using(ceoID) where symbol = %s;", [symbol])
            self.displayData(result)
            result = read_query(self.connection, """select cityName as 'city', countryName as 'state/country' from StateCountry inner join CityInCountry using(stateCountryID)
                inner join City using(cityID) inner join CompanyInCity using(cityID) where symbol = %s;""", [symbol])
            self.displayData(result)
            result = read_query(self.connection, """select industryName as 'industry', sectorName as 'sector' from Sector inner join IndustryInSector using(sectorID)
                inner join Industry using(industryID) inner join CompanyInIndustry using(industryID) where symbol = %s;""", [symbol])
            self.displayData(result)

        elif (choice == "2"):
            print(line + "Lookup company yearly performance data"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            year = self.determineYear()
            result = read_query(self.connection, "select * from YearlyData where symbol = %s and year = %s", [symbol, year])
            self.displayData(result)

        elif (choice == "3"):
            print(line + "Lookup stock daily data"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            date = self.determineDate()
            query = """with temp as (select * from DailyData where symbol = %s)
                        select * from temp where date = %s;"""
            result = read_query(self.connection, query, [symbol, date])
            self.displayData(result)
            
        elif (choice == "4"):
            print(line + "Lookup specific stock's latest data"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            query = """with temp as (select * from DailyData where symbol = %s)
                        select * from temp where date = (select max(date) from temp);"""
            result = read_query(self.connection, query, [symbol])
            self.displayData(result)

        elif (choice == "5"):
            print(line + "Find articles about company"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            query = "select * from AnalystInfo where symbol = %s order by date limit 5;"
            result = read_query(self.connection, query, [symbol])
            self.displayData(result)
            
        elif (choice == "6"):
            print(line + "View comments about company"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            query = "select * from Comments where symbol = %s limit 5"
            result = read_query(self.connection, query, [symbol])
            self.displayData(result)   

        else:
            iipak()
            return

        pak()
        
        
        
    def update(self):
        self.prefix = "[update mode] "
        print()
        print("--------------------- Update Mode ---------------------")
        choiceList = """
        1. Update company name
        2. Update company ceo
        3. Update employee count
        4. Update fiscal end date
            """
        print(choiceList)
        choice = input(self.prefix + "Enter selection number: ")
        
        line = "-------"
        
        if (choice == "1"):
            print(line + "Update company name"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            newName = input("Enter new company name: ")
            if (self.validateInput(newName, "companyName")):
                print("Company name already exists")
                pak()
                return
            query = "update Company set name = %s where symbol = %s;"
            execute_query(self.connection, query, [newName, symbol])

        elif (choice == "2"):
            print(line + "Update company ceo"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            newCeo = input("Enter the ceo's new name: ")
            newAge = inputInt("Enter the ceo's new age: ")
            query = "select * from CEO where name = %s;"
            nameInCEO = read_query(self.connection, query, [newCeo])
            # if input name is not in the ceo table, first add name to CEO table, then to CEOruns
            if (len(nameInCEO) == 0):
              query = "insert into CEO (name, age) values (%s, %s)" 
              execute_query(self.connection, query, [newCeo, newAge])
              query = "select * from CEO where name = %s;"
              nameInCEO = read_query(self.connection, query, [newCeo])
              
            ceoID = (nameInCEO[0]).get('ceoID')
            query = "update CEOruns set ceoID = %s where symbol = %s;"
            execute_query(self.connection, query, [ceoID, symbol])
            
        elif (choice == "3"):
            print(line + "Update employee count"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            empCount = inputInt("Enter new number of employees: ")
            query = "update Company set employees = %s where symbol = %s;"
            execute_query(self.connection, query, [empCount, symbol])
            
        elif (choice == "4"):
            print(line + "Update fiscal end date"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            newDate = input("Input fiscal end date (eg: '18-Oct'): ")
            query = "update Company set fiscalDateEnd = %s where symbol = %s;"
            execute_query(self.connection, query, [newDate, symbol])
            
        else:
            iipak()
            return

        pak()
        
            
    def insert(self):
        self.prefix = "[insert mode] "
        print()
        print("--------------------- Insert Mode ---------------------")
        choiceList = """
            1. Add new company
            2. Add stock daily data for a specific company
            3. Add yearly performance data for specific company
            4. Add new article
            5. Add comment
            """
        print(choiceList)
        choice = input(self.prefix + "Enter selection number: ")
        line = "------"
        if (choice == "1"):
            print(line + "Add new company"+ line)
            symbol = input("Enter ticker symbol: ")
            if (self.validateInput(symbol, "symbol")):
                print("Symbol already exists")
                pak()
                return

            companyName = input("Enter company name: ")
            if (self.validateInput(companyName, "companyName")):
                print("Company name already exists")
                pak()
                return

            sector = input("Enter sector to which the company belongs to: ")
            industry = input("Enter industry to which the company belongs to: ")
            summaryQuote = input("Enter summaryQuote link: ")
            ceoName = input("Enter ceo name: ")
            ceoAge = inputInt("Enter ceo age: ")
            city = input("Which city are the company headquarters in: ")
            country = input("Which country is the company headquarters in: ")
            
            print("Enter fiscal end date: ", end='')
            fiscalDateEnd = input("Input fiscal end date (eg: '18-Oct'): ")
            employees = inputInt("Number of employees in company: ")
            yearFounded = inputInt("Enter year founded (no future dates allowed): ")
                
            query = """insert into Company (symbol, name, summaryQuote, fiscalDateEnd, employees, yearFounded) values (%s, %s, %s, %s, %s, %s);"""
  
            params = [symbol, companyName, summaryQuote, fiscalDateEnd, employees, yearFounded]
            
            execute_query(self.connection, query, params)
        
            #add to city to city table
            res = read_query(self.connection, "select * from StateCountry where countryName = %s;", [country])
            DNE = 0
            if (len(res) == 0):
              	# if both city and country DNE
                execute_query(self.connection, "insert into StateCountry (countryName) values (%s);", [country])
                execute_query(self.connection, "insert into City (cityName) values (%s);", [city])
                DNE = 1
                
            else:
                res = read_query(self.connection, "select * from City where cityName = %s;", [city])
                if (len(res) == 0):
                    #if city DNE but country present
                    execute_query(self.connection, "insert into City (cityName) values (%s);", [city])
                    DNE = 1

            res = read_query(self.connection, "select stateCountryID from StateCountry where countryName = %s;", [country])
            countryID = (res[0]).get('stateCountryID')

            res = read_query(self.connection, "select cityID from City where cityName = %s;", [city])
            cityID = (res[0]).get('cityID')
            
            if (DNE):
              	execute_query(self.connection, "insert into CityInCountry (stateCountryID, cityID) values (%s, %s);", [countryID ,cityID])
                
            execute_query(self.connection, "insert into CompanyInCity (symbol, cityID) values (%s, %s);", [symbol, cityID])
                
                      
            #industry sector
            DNE = 0
            res = read_query(self.connection, "select * from Sector where sectorName = %s;", [sector])
            if (len(res) == 0):
                execute_query(self.connection, "insert into Sector (sectorName) values (%s);", [sector])
                execute_query(self.connection, "insert into Industry (industryName) values (%s);", [industry])
                DNE = 1
            
            else:
                res = read_query(self.connection, "select * from Industry where industryName = %s;", [industry])
                if (len(res) == 0):
                    execute_query(self.connection, "insert into Industry (industryName) values (%s);", [industry])
                    DNE = 1
            	
            res = read_query(self.connection, "select sectorID from Sector where sectorName = %s", [sector])
            sectorID = (res[0]).get('sectorID')

            res = read_query(self.connection, "select industryID from Industry where industryName = %s", [industry])
            industryID = (res[0]).get('industryID')
            
            if (DNE):
                execute_query(self.connection, "insert into IndustryInSector (sectorID, industryID) values (%s, %s);", [sectorID, industryID])
              
            execute_query(self.connection, "insert into CompanyInIndustry (symbol, industryID) values (%s, %s);", [symbol, industryID])
            
            
            # ceo stuff
            nameInCEO = read_query(self.connection, "select * from CEO where name = %s;", [ceoName])
            # if input name is not in the ceo table, first add name to CEO table, then to CEOruns
            if (len(nameInCEO) == 0):
                execute_query(self.connection, "insert into CEO (name, age) values (%s, %s)" , [ceoName, ceoAge])
                nameInCEO = read_query(self.connection, "select ceoID from CEO where name = %s;", [ceoName])
                
            ceoID = (nameInCEO[0]).get('ceoID')
            execute_query(self.connection, "insert into CEOruns (ceoID, symbol) values (%s, %s);", [ceoID, symbol])
            
                        
        elif (choice == "2"):
            print(line + "Add stock daily data for a specific company"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            print("Enter date: ", end='')
            date = self.determineDate()
            volume = inputInt("Enter volume traded: ")
            openPrice = inputDecimal("Enter price at opening: ")
            highPrice = inputDecimal("Enter the price high: ")
            lowPrice = inputDecimal("Enter the price low: ")
            closePrice = inputDecimal("Enter price at closing: ")
            adjclosePrice = inputDecimal("Enter adjclose price: ")
            query = """INSERT INTO DailyData (date, volume, open, high, low, close, adjclose, symbol)
            		VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
            params = [date, volume, openPrice, highPrice, lowPrice, closePrice, adjclosePrice, symbol]
            execute_query(self.connection, query, params)
            
        elif (choice == "3"):            
            print(line + "Add yearly performance data for specific company"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            year = inputInt("Enter year (no future dates allowed): ")
            if (self.yearExists(year, symbol)): 
                print(str(year) + " yearly performance data for "+ symbol +" already exists.")
                pak()
                return

            revenue = inputInt("Enter yearly revenue: ")
            revenueGrowth = inputDecimal("Enter yearly revenue growth: ")
            netIncome = inputInt("Enter yearly netIncome: ")
            eps = inputDecimal("Enter earnings per share: ")
            freeCashFlowMargin = inputDecimal("Enter free cash flow margin: ")
            netProfitMargin = inputDecimal("Enter net profit margin: ")
            currentRatio = inputDecimal("Enter current ratio: ")
            returnOnEquity = inputDecimal("Enter return on equity amount: ")
            PEratio = inputDecimal("Enter price to earnings ratio: ")
            revenuePerShare = inputDecimal("Enter revenue per share: ")
            marketCap = inputInt("Enter market cap: ")
            dividendYield = inputDecimal("Enter dividend yield: ")
            ROIC = inputDecimal("Enter ROIC: ")
            threeYrRevenueGrowth = inputDecimal("Enter 3 year revenue growth: ")

            query = """insert into YearlyData (symbol, revenue, revenueGrowth, netIncome, eps, freeCashFlowMargin, netProfitMargin, currentRatio, returnOnEquity, PEratio, revenuePerShare, marketCap,
                                              dividendYield, ROIC, 3yrRevenueGrowth, year) 
                                              values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            
            params = [symbol, revenue, revenueGrowth, netIncome, eps, freeCashFlowMargin, netProfitMargin, currentRatio, returnOnEquity, PEratio, revenuePerShare, marketCap,
                                              dividendYield, ROIC, threeYrRevenueGrowth, year];
                                              
            execute_query(self.connection, query, params)
              
  
        elif (choice == "4"):
            print(line + ""+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            headline = input("Enter comment: ")
            currDate = datetime.datetime.today()
            query = "INSERT INTO ArticleInfo (headline, date, symbol) VALUES (%s, %s, %s);"
            execute_query(self.connection, query, [headline, currDate, symbol])
            
        elif (choice == "5"):
            print(line + "" + line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            commentText = input("Enter comment: ")
            currDate = datetime.datetime.today()
            query = "INSERT INTO Comments (symbol, commentText, date) VALUES (%s, %s, %s);"
            execute_query(self.connection, query, [symbol, commentText, currDate])
            
        else:
            iipak()
            return
        
        pak()
  
    def delete(self):
        self.prefix = "[delete mode] "
        print()
        print("--------------------- Delete Mode ---------------------")
        choiceList = """
            1. Delete company
            2. Delete ceo
            3. Delete comment
            4. Delete article
              """
        print(choiceList)
        choice = input(self.prefix + "Enter selection number: ")

        line = "-------"

        if (choice == "1"):
            print(line + "Delete company"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            
            query = "delete from CompanyInCity where symbol=%s;"
            execute_query(self.connection, query, [symbol])
            
            query = "delete from CompanyInIndustry where symbol=%s;"
            execute_query(self.connection, query, [symbol])
            
            query = "delete from CEOruns where symbol=%s;"
            execute_query(self.connection, query, [symbol])
            
            query = "delete from Company where symbol=%s;"
            execute_query(self.connection, query, [symbol])

        elif (choice == "2"):
            print(line + "Delete ceo"+ line)
            symbol = self.determineCompanyStrict()
            if (symbol == -1):
                return
            
            res = read_query(self.connection, "select ceoID from CEOruns where symbol=%s", [symbol])
            ceoID = (res[0]).get('ceoID')
            query = "delete from CEO where ceoID=id;"
            execute_query(self.connection, query, [ceoID])
            
            query = "delete from CEOruns where symbol=%s";
            execute_query(self.connection, query, [symbol])
            
        elif (choice == "3"):
            print(line + "Delete comment"+ line)
            commentID = input("Enter the comment ID of the comment you wish to delete: ")
            query = "delete from Comments where commentID= %s;"
            execute_query(self.connection, query, [commentID])

        elif (choice == "4"):
            print(line + "Delete article"+ line)
            articleID = input("Enter the article ID of the article you wish to delete: ")
            query = "delete from AnalystInfo where articleID= %s;"
            execute_query(self.connection, query, [articleID])

        else:
            iipak()
            return

        pak()
    
    

    def determineCompany(self):
        while(True):
            mode = input("To search for company using company name enter '1', if using symbol enter '2', (a valid symbol is 'A'):  :  ")
            if (mode == "1"):
                val = input("Enter company name: ")
                if (self.validateInput(val,"companyName")):
                    query = "select symbol from Company where name = %s"
                    results = read_query(self.connection, query, [val])     
                    return (results[0]).get('symbol')
                else:
                    cpak("'"+ val + "' company does not exist. Try again...")
                    continue
            elif (mode == "2"):
                val = input("Enter symbol: ")
                val = val.upper()
                if (self.validateInput(val,"symbol")):
                    return val
                else:
                    cpak("'"+ val + "' company does not exist. Try again...")
                    continue
            else:
                iipak()
                
    def determineCompanyStrict(self):
        mode = input("To search for company using company name enter '1', if using symbol enter '2', (a valid symbol is 'A'): ")
        
        if (mode == "1"):
            val = input("Enter company name: ")
            if (self.validateInput(val,"companyName")):
                query = "select symbol from Company where name = %s"
                results = read_query(self.connection, query, [val])     
                return (results[0]).get('symbol')
            else:
                cpak("'"+ val + "' company does not exist.")
                return -1
        elif (mode == "2"):
            val = input("Enter symbol: ")
            val = val.upper()
            if (self.validateInput(val,"symbol")):
                return val
            else:
                cpak("'"+ val + "' company does not exist.")
                return -1
        else:
            iipak()
            return -1

        
    
    def validateInput(self,val,iType):
        #search for val using query
        if (iType == "companyName"):
            res = read_query(self.connection, "select symbol from Company where name = %s",[val])
            if (len(res) > 0):
                return True
        elif (iType == "symbol"):
            res = read_query(self.connection, "select symbol from Company where symbol = %s",[val])
            if (len(res) > 0):
                return True
        return False
        
    def determineYear(self):
        while(True):
            userIn = input("Enter year (between 2014 and 2018): ")
            validYears = ["2014","2015","2016","2017","2018"]
            if (userIn in validYears):
                return userIn
            else:
                iipak()

    def determineDate(self):
        while(True):
            print("Enter date (no future dates accepted): ")
            year = inputInt('Enter year (YYYY): ')
            month = inputInt('Enter month (MM): ')
            day = inputInt('Enter day (DD): ')
            givenDate = datetime.datetime(year, month, day)
            currDate = datetime.datetime.today()
            if (givenDate < currDate):
                return givenDate
            else:
                print("Future day inputed!")
                iipak()

    def yearExists(self, year, symbol):
        query = "select distinct year from YearlyData where symbol = %s;"
        result = read_query(self.connection, query, [symbol])
        for elem in result:
            y = elem.get['year']
            if (y == year):
                return True
        return False
    
    def displayDailyData(self, data):
        print("daily data")

    def displayCompanyData(self, res):
        print("\n")
        for row in res:
            for key, value in row.items():
                print(key+": "+ str(value))
            print("\n")

    def displayData(self, res):
        if (len(res) == 0):
            print("\nNo results!")
            return
        print("\n")
        for row in res:
            for key, value in row.items():
                print("\n"+ key + ": " + str(value))
    
# =============================== Helper functions ===============================    

def pak():
    input("\nPress any key to continue...")
   
def iipak():
    input("\nInvalid input. Press any key to continue...")

def cpak(text):
    input("\n"+text)

def inputInt(text):
    while (True):
        raw = input(text)
        error = 0
        try:
            val = int(raw)
        except ValueError:
            iipak()
            error = 1
        if (error == 0): 
            return val

def inputDecimal(text):
    while (True):
        raw = input(text)
        error = 0
        try:
            val = float(raw)
        except ValueError:
            iipak()
            error = 1
        if (error == 0): 
            return val


# =============================== Functions to access database ===============================  
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Server connection successful")
    except Error as err:
        print(f"Error: {err}")

    return connection

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: {err}")

    return connection

def execute_query(connection, query, params):
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        connection.commit()
    except Error as err:
        print(f"Error: {err}")
        return

    print("Modification was successful!")

def print_query(connection, query, params):
    cursor = connection.cursor(dictionary=True)
    results = None
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        for result in results: 
            print(result)
        return results
    except Error as err:
        print(f"Error: {err}")


def read_query(connection, query, params):
    cursor = connection.cursor(dictionary=True)
    results = None
    try:
        cursor.execute(query, params)
        results = cursor.fetchall()
        return results
    except Error as err:
        print(f"Error: {err}")        

  

# =============================== Run ===============================
stonkApp = ClientApp()
stonkApp.mainmenu()

