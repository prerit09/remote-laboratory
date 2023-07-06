import requests
from flask import Flask, redirect, url_for, render_template, request


def result(code, input, expected=None):
    if(request.method == "POST"):
        url = "http://localhost:2358/submissions?wait=true"
        
        if expected is not None:
            data = {
                "source_code": code,
                "language_id": "52",
                "stdin": input,
                "expected_output" : expected
            }
        else:
            data = {
                "source_code": code,
                "language_id": "52",
                "stdin": input,
            }
        # print(data)
        
        response = requests.post(url, json=data)
        
        x = response.json()
        
        token = x['token']
        
        output = requests.get("http://localhost:2358/submissions/"+str(token))
        # print(output.json())
        
        # json_output = output.json()

        # out = "Output : \n" + json_output[
        #     'stdout'] + "\n\nTime Taken : " + json_output[
        #     'time'] + "\n\nError : " + str(json_output[
        #     'stderr']) + "\n\n Status : The code is " + str(
        #     json_output['status']['description'])
        
        # out = out.replace('\n', '<br>')
        print("here sis op")
        print(output.json())
        return output.json()