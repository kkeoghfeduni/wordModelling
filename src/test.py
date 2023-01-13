import utilities
import os

def test_sampleForXdaysNTimes():
    bookPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Books'
    convoPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Convos'

    finalList = utilities.sampleGroupForXdaysNTimes(365, bookPath, 1, convoPath, 4, 10)
    

test_sampleForXdaysNTimes()
