Start-Process powershell -ArgumentList "py -m src.main"
Start-Process powershell -ArgumentList "py test/test_websocket_client.py"