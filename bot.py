import xkcd
from matrix_client.client import MatrixClient

USERNAME = "insert the bots username here"
PASSWORD = "insert the bots password here"
SERVER = "https://matrix.org"


def send_xkcd(room):
    """Downloads random xkcd comic, uploads it to the server and sends the link into room.

    :param room: Matrix room where the XKCD was requested
    """
    print('Sending XKCD')
    xkcd.getRandomComic().download(output='.', outputFile='xkcd.jpg')
    with open("xkcd.jpg", "rb") as f:
        data = f.read()
    url = client.upload(data, 'image/jpeg')
    room.send_image(url, 'xkcd.jpg')


def handle_message(room, event):
    """This function handles incoming matrix events and reacts on the keyword xkcd.

    :param room: Matrix room where message event occurred
    :param event: Matrix event of the message
    """
    # Make sure we didn't send this message ourselves
    print(event)
    if "@" + USERNAME in event['sender']:
        return
    try:
        if not event['content']['msgtype'] == 'm.text':
            print('No text message, ignoring...')
            return
        text = event['content']['body']
    except KeyError:
        print('Cannot handle that request')
        return
    print('Received: %s' % text)
    if text.startswith('xkcd'):
        send_xkcd(room)


def handle_invite(room_id, state):
    """This function handles new invites to Matrix rooms by accepting them.

    :param room_id: Matrix room is
    :param state: State of the Matrix room
    """
    room = client.join_room(room_id)
    room.add_listener(handle_message)


if __name__ == '__main__':
    client = MatrixClient(SERVER)
    client.login_with_password(USERNAME, PASSWORD)
    print('Login as %s successful' %USERNAME)
    client.add_invite_listener(handle_invite)
    for _, room in client.get_rooms().items():
        room.add_listener(handle_message)
    client.start_listener_thread()
    while True:
        input()
