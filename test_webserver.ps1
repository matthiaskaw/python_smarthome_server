Start-Process powershell -ArgumentList '-NoExit -Command "py -m src.main"'
Start-Process powershell -ArgumentList '-NoExit -Command "py test/test_websocket_client.py"'