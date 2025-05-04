# Login and generate OTP
curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d '{"mobile": "+989121234567"}'

# Get current time (this will increment the counter)
curl -X GET http://localhost:8000/api/now/ -H "Authorization: +989121234567" 

# Get stats for the user
curl -X GET http://localhost:8000/api/stats/ -H "Authorization: +989121234567"
