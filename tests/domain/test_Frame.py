from webcamrecorder.domain import VideoSource


def test():
    source = VideoSource.VideoSource("d:\\20230421_063552_43分ころゴミ捨てられる.mp4")
    frame = source.createFrame(10900)
    bytes = frame.encode()

    assert True
