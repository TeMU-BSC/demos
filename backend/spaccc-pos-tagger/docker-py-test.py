import docker, tarfile
from io import BytesIO

def test_send_data_via_stdin_into_container():
    client = docker.APIClient()

    # pull image
    client.pull('busybox:latest')

    # create container
    container = client.create_container(
        'busybox',
        stdin_open = True,
        command    = 'sh -c "cat - >/received.txt"')
    client.start(container)

    # attach stdin to container and send data
    original_text_to_send = 'hello this is from the other side'
    s = client.attach_socket(container, params={'stdin': 1, 'stream': 1})
    s._sock.send(original_text_to_send.encode('utf-8'))
    s.close()

    # stop container and collect data from the testfile
    client.stop(container)
    client.wait(container)
    raw_stream,status = client.get_archive(container,'/received.txt')
    tar_archive = BytesIO(b"".join((i for i in raw_stream)))
    t = tarfile.open(mode='r:', fileobj=tar_archive)
    text_from_container_file = t.extractfile('received.txt').read().decode('utf-8')
    client.remove_container(container)

    # check for equality
    assert text_from_container_file == original_text_to_send

if __name__ == '__main__':
    test_send_data_via_stdin_into_container()