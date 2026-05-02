import requests,sqlite3,argparse,time

parser = argparse.ArgumentParser()
parser.add_argument(
      '--url',
      dest='url',
      default='https://volby.transparency.sk/financovanie/darcovia/', 
      help='Url of page to process')
args = parser.parse_args()
#add url as an argument

connection = sqlite3.connect('db.sqlite3')
cursor = connection.cursor()
cursor.execute("""DROP TABLE IF EXISTS donors""")
cursor.execute("""DROP TABLE IF EXISTS parties""")
cursor.execute("""DROP TABLE IF EXISTS donations""")

cursor.execute("""CREATE TABLE donors (
  user_id INT,
  name TEXT,
  type TEXT,
  sex TEXT,
  city TEXT,
  region TEXT,
  region_long TEXT
               )""")
#TODO najst ktore politicke strany podporil jednotlivy kandidat..

cursor.execute("""CREATE TABLE parties (
  party_id INT,
  name TEXT
               )""")
#TODO later add info about political parties (SOMEHOW)
cursor.execute("""CREATE TABLE donations (
  donate_id INT,
  party_id INT,
  date TEXT,
  user_id INT,
  user_type TEXT,
  sex TEXT,
  city TEXT,
  region TEXT,
  income_type TEXT,
  amount INT,
  flag TEXT,
  source TEXT
               )""")
#connect to database and clear its contents before you start anything

max_pages = 222
api_url = "https://volby.transparency.sk/api/donors/donations.php"

headers = {
    'User-Agent': 'Mozilla/5.0'
}
all_data = []
limit = 100

income_type_map = {
    1: "bezodplatné plnenie",
    2: "členský príspevok",
    3: "finančný dar",
    4: "nepeňažný dar",
    5: "pôžička",
    6: "úver",
    7: "zmluvné dojednanie"
}
flag_map = {
    0: None,
    1: "veľký dar",
    2: "veľká pôžička",
    3: "vysoké bezodplatné plnenie"
}
region_map = {
    "BA": "Bratislavský",
    "TT": "Trnavský",
    "TN": "Trenčiansky",
    "NR": "Nitriansky",
    "ZA": "Žilinský",
    "BB": "Banskobystrický",
    "PO": "Prešovský",
    "KE": "Košický"
}
page_counter = 0
donor_counter = 1
party_counter = 1
donation_counter = 1
unknown_counter = 1

while page_counter < max_pages:
  params = {'b': limit, 'o': page_counter, 's': 'date'}
  try:
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
  
    data = response.json()
    all_data.extend(data)
    donations = data.get('rows', [])
    for donation in donations:
      party_name = donation[0]
      date = donation[1]
      if donation[2] == "": #if name of person doesnt exist in this donation
        user_type = "firma"
        user_name = donation[4] #name of company
      else:
        user_type = "fyzická osoba"
        user_name = donation[2]
        if "neznáme" in user_name:
          user_name = "Neznámy darca" + str(unknown_counter) #think about how to do it better. or just throw it out? mention in report.
          unknown_counter +=1

      city = donation[5]
      income_type = income_type_map.get(donation[6])
      amount = round(donation[8],2)
      source = donation[9]
      sex = donation[11] if donation[2] != "" else None #give NULL to companies

      region = donation[12]
      region_long = region_map.get(region) if region != "" else ""
      flag = flag_map.get(donation[13])

      user_exists = cursor.execute("SELECT name FROM donors WHERE name = (?) AND city = (?)",(user_name,city)).fetchone()
      if not user_exists: #we didnt meet this donor previously
        cursor.execute("INSERT INTO donors (user_id,name,type,sex,city,region,region_long) VALUES (?,?,?,?,?,?,?)",
                        (donor_counter,user_name,user_type,sex,city,region,region_long))
        connection.commit()
        donor_counter += 1
      
      party_exists = cursor.execute("SELECT name FROM parties WHERE name = (?)",(party_name,)).fetchone()
      if not party_exists:
        cursor.execute("INSERT INTO parties (party_id, name) VALUES (?,?)",(party_counter,party_name))
        connection.commit()
        party_counter += 1
      party_id = cursor.execute("SELECT party_id FROM parties WHERE name = (?)",(party_name,)).fetchall()[0][0]
      user_id = cursor.execute("SELECT user_id FROM donors WHERE name = (?) AND city = (?)",(user_name,city)).fetchall()[0][0]
      cursor.execute("INSERT INTO donations (donate_id,party_id,date,user_id,user_type,sex,city,region,income_type,amount,flag,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                      (donation_counter,party_id,date,user_id,user_type,sex,city,region,income_type,amount,flag,source))  
      connection.commit()
      donation_counter += 1  
  except Exception as e:
    print(f"Error on page {page_counter}: {e}")
    break

  time.sleep(1)
  page_counter+=1