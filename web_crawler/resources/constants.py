#global constants

URL_MONITOR_NAMESPACE = 'YousafNameSpace'

URL_MONITOR_METRIC_NAME_AVAILABILITY = 'url_availability'

URL_MONITOR_METRIC_NAME_LATENCY = 'url_latency'

websites= ["skipq.org", "github.com", "facebook.com"]

Synth_Commands = ["cd Yousaf_Aftab/Sprint_5", 
            "pip install -r requirements.txt", 
            "npm install -g aws-cdk",
            "cdk synth"
            ]

Pipeline_output_directory = "Yousaf_Aftab/Sprint_5/cdk.out"

Unit_test_commands = ["cd Yousaf_Aftab/Sprint_5",
        "pip install -r requirements.txt",
        " pip install pytest",
        "npm install -g aws-cdk", 
        "pytest tests/unit/test_sprint_4_stack.py"]

Integration_Test_commands = [ "cd Yousaf_Aftab/Sprint_5",
        "pip install pytest",
        "pip install -r requirements.txt",
        "npm install -g aws-cdk",
        "pytest tests/integration/test_httpreq_dynamodb.py"]