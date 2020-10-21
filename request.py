import requests
r = requests.post('http://18.141.207.232:8888//predict', json = {
"Store":1111,
"DayOfWeek":4,
"Date":"2014-07-10",
"Customers":410,
"Open":1,
"Promo":0,
"StateHoliday":"0",
"SchoolHoliday":1
})
print(r.text)