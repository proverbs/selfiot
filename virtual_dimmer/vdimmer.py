## DON'T KNOW HOW TO WRITE SYNC CLIENT

# import asyncio
# import websockets

# async def dimmer_controller():
#     uri = "ws://localhost:8000/ws/dimmer/qwer/"
#     async with websockets.connect(uri) as websocket:
#         while True:
#             # this could be problematic because of async functions
#             cmd = await websocket.recv()
#             # print(f"<<< {cmd}")

#             resp = '{"message": "{cmd} success"}'

#             await websocket.send(resp)
#             print(f">>> {resp}")

# asyncio.get_event_loop().run_until_complete(dimmer_controller())





## THE CONNECTION WILL CLOSE AFTER THE FIRST SEND. DON'T KNOW WHY.

# import websocket

# def on_message(ws, cmd):
#     print(f'<<< {cmd}')
#     resp = '{"message": "%s success"}' % cmd
#     ws.send(resp)
#     print(f">>> {resp}")

# def on_error(ws, error):
#     print(error)

# def on_close(ws):
#     print("### closed ###")

# def on_open(ws):
#     ws.send('{"message": "success: connected"}')


# websocket.enableTrace(True)
# uri = "ws://localhost:8000/ws/dimmer/qwer/"
# ws = websocket.WebSocketApp(uri,
#                             on_message=on_message,
#                             on_error=on_error,
#                             on_close=on_close)
# ws.on_open = on_open
# ws.run_forever()




from websocket import create_connection

# TODO: change to hostname, how to get the dimmer name?
uri = "ws://www.proverbs.top:8765/ws/dimmer/device_1/"

ws = create_connection(uri)
# print("success")

while True:
    cmd =  ws.recv()
    resp = '{"message": "success"}'
    ws.send(resp)
    print(cmd)

ws.close()