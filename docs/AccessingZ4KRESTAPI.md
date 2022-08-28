# Accessing the Z4K REST API

#### With Z4K Ingress

To access the Z4K API if you're using Z4K ingress, run the command:

```
   kubectl get services -n <z4k namespace>
```

#### With External Ingress

To access the Z4K API if you're using external ingress, use the following steps.

1)  Copy an EXTERNAL-IP/Loadbalancer-IP value into browser and add the /zkm/api/help:

      https://![](https://img.shields.io/static/v1?label=&message=a11ed2fcc9d734cf594793d044753d97-1234567.eu-central-1.elb.amazonaws.com&color=blue)/zkm/api/help

      This will authorize you to run Swagger commands. 

2)  Prepare an access token:
```
curl --location --request POST 'https://<EXTERNAL-IP or loadbalancer-IP>/auth/realms/zerto/protocol/openid-connect/token' \
--data-urlencode 'username=keycloack username' \
--data-urlencode 'password=password' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'client_id=admin-cli'
```

   You'll receive an access_token in response, similar to the following: 

```
{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJSW05NnpxZUN0ajF6TVhkVk83WHMyYzJmNnE4b3BsNG5kelZlWHpMT3FzIn0.
eyJleHAiOjE2NTkyNjg0MjMsImlhdCI6MTY1OTI2ODEyMywianRpIjoiOGRlNTlkZDUtYTJkMy00OGYzLWIzOTAtZWMxNjliOGM2MzA1IiwiaXNzIjoiaHR0cHM6Ly9hZ
TIyMjViNjU3NWFhNGVjNmE4OGI1YTUzYTc0MzcxYy0xMTE2NDg5NDkwLmV1LWNlbnRyYWwtMS5lbGIuYW1hem9uYXdzLmNvbS9hdXRoL3JlYWxtcy96ZXJ0byIsInN1Yi
I6IjQyYTIwZTM3LTliMTUtNDQwMC1hOWNiLWYzOGVmMjRjZGZhYiIsInR5cCI6IkJlYXJlciIsImF6cCI6ImFkbWluLWNsaSIsInNlc3Npb25fc3RhdGUiOiIzMTdkMmE
3ZS0wODI2LTQxMTktOTJlYi1lZDBlMmYyMjI2YTIiLCJhY3IiOiIxIiwic2NvcGUiOiJlbWFpbCBwcm9maWxlIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJuYW1lIjoi
YWRtaW4iLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG1pbiIsImdpdmVuX25hbWUiOiJhZG1pbiJ9.nx6CB1jQjUJ72oKWyiFAq6NYlYX6OdwSL7KD5Og4ME_jV9Ufr6
Oj9q0jqqSBDHQOgEamI3oztROhPP4BJRsZ5TRqa_DS-zImGb7cNxCMrKM-0m4OjqFScuTg_lUAA_ItkjWJutrNpfwVxSW4-WUHjbGqZBTiZcaRTBZDCWw6rqeSXaCNSSU
6Nztl85jmFBw7lA2ecSrB7lt1oQS4XBCBDrjxZc7CV-qx4npuRP9Xh70WY_D4wPRwCYegvymUm3sDa96KrCbXWJkbOTOmCx8MSJaRKTPNoWIddUW7_pd7h8iLDQkBXJu
GbE_c6-hPhsVKwfkxrl1a-MHpwTcf-13lA","expires_in":300,"refresh_expires_in":1800,"refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiS
ldUIiwia2lkIiA6ICI2ZDNlYzk
xNy1jOTc2LTRhZGEtOWIwMC1mNjY2YjU4ZTFiZjkifQ.eyJleHAiOjE2NTkyNjk5MjMsImlhdCI6MTY1OTI2ODEyMywianRpIjoiOTExNzhkYTYtMzM5YS00MWZlLWI2
YjYtYjQ0YzRlMThjMTI1IiwiaXNzIjoiaHR0cHM6Ly9hZTIyMjViNjU3NWFhNGVjNmE4OGI1YTUzYTc0MzcxYy0xMTE2NDg5NDkwLmV1LWNlbnRyYWwtMS5lbGIuYW1he
m9uYXdzLmNvbS9hdXRoL3JlYWxtcy96ZXJ0byIsImF1ZCI6Imh0dHBzOi8vYWUyMjI1YjY1NzVhYTRlYzZhODhiNWE1M2E3NDM3MWMtMTExNjQ4OTQ5MC5ldS1jZW50cmF
sLTEuZWxiLmFtYXpvbmF3cy5jb20vYXV0aC9yZWFsbXMvemVydG8iLCJzdWIiOiI0MmEyMGUzNy05YjE1LTQ0MDAtYTljYi1mMzhlZjI0Y2RmYWIiLCJ0eXAiOiJSZWZyZ
XNoIiwiYXpwIjoiYWRtaW4tY2xpIiwic2Vzc2lvbl9zdGF0ZSI6IjMxN2QyYTdlLTA4MjYtNDExOS05MmViLWVkMGUyZjIyMjZhMiIsInNjb3BlIjoiZW1haWwgcHJvZmls
ZSJ9.JZ07dDaxYyUfbxI1vHbe2KDYpyVbkbxcBc1wk4qk40A","token_type":"Bearer","not-before-policy":0,"session_state":"317d2a7e-0826-4119-
92eb-ed0e2f2226a2","scope":"email profile"}% 
```
3)  Copy the access_token value.
4)  Click **Authorise**.
5)  In the **Available authorization** dialog, in the **Value** field type "Bearer" and paste the access_token.
