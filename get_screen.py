from win32api import GetSystemMetrics

def get_wh():
    print 'width:' + str(GetSystemMetrics(0))
    print 'height:' + str(GetSystemMetrics(1))

    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)

    return width,height
