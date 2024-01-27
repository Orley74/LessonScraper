import requests
import scrapydo

client = requests.session()
# url = 'http://127.0.0.1:8000/polls/grp'

# client = requests.session()
# z=client.get('http://127.0.0.1:8000/polls/')
# Django would like the csrf token passed with the data, so we do need to save it off seperately.
# csrftoken = client.cookies['csrftoken']

groups_key = {'key': 'karzel'}
groups = client.options('https://planwat.azurewebsites.net/polls/grp', headers=groups_key)
# groups = client.get('http://old.wcy.wat.edu.pl/')

# print(groups.content)
# payload = {'key': 'karzel', 'grp': 'WCY20IK1S0', 'Confirm': 'tak'}
# i = 1
# # for group in grupy:
# #     if group == "- Wybierz grup\u0119 -":
# #         continue
# #     payload['grp'] = group
# #     print(f"pobieram grupe {i}\{len(grupy)}: {group}")
# #     i+=1
# #     r = client.post('https://planwat.azurewebsites.net/polls/plan/stud', headers=payload)
# #     print(r.text)
client.close()
print(groups.text)