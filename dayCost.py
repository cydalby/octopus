import requests
from requests.auth import HTTPBasicAuth
import datetime

baseurl = "https://api.octopus.energy/v1/"

# Set the API key, meter MPAN and serial
key = "sk_live_EyaMavRzk1kDkCjjCsYkDq2M"
MPAN = "2500020919260"
serial = "19L2717574"

# Set the peak and off-peak rates for Octopus Go
ratesUrl = baseurl + "products/GO-VAR-22-10-14/electricity-tariffs/E-1R-GO-VAR-22-10-14-M/standard-unit-rates/"
rates = requests.get(ratesUrl,auth=HTTPBasicAuth(key,"")).json()

offpeakrate = rates["results"][1]['value_inc_vat']
peakrate = rates["results"][0]['value_inc_vat']

today = datetime.date.today()

peakusage = 0
offpeakusage = 0
fromdate = (today - datetime.timedelta(1)).isoformat()
todate = (today - datetime.timedelta()).isoformat()

url = baseurl + "electricity-meter-points/" + MPAN + "/meters/" + serial + "/consumption" + "?period_from=" + fromdate + "&period_to=" + todate 
consumption = requests.get(url,auth=HTTPBasicAuth(key,"")).json()

i = 0 # Used to index the results returned (48 results per day, one per 30 minutes)
for result in consumption["results"]: # Loop through the results returned for the specified day, extract the peak and off-peak units consumed and calculate the cost
    if i in range(40,47): # These are the indexes of the off-peak hours (00:30-04:30)
        offpeakusage = offpeakusage + result["consumption"]
    else:
        peakusage = peakusage + result["consumption"]
    i += 1

# Calculate the peak / off-peak and total cost for the day in £'s (rounded to 2 decimal places)
peakcost = round((peakusage * peakrate / 100), 2)
offpeakcost = round((offpeakusage * offpeakrate / 100), 2)
totalcost = round((peakcost + offpeakcost), 2)

print("£" + (str(totalcost)))