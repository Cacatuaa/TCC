# Necessary libraries
import cv2
from collections import Counter

# Function to verify where is the begin and it's respective end
def findBeginEnd(array, value):
    begin = array.index(value) # Get the first index of the value
    array.reverse() # Reverse the array to find the last index
    end = array.index(value) # Get the last index of the value
    end = (len(array) - 1) - end # Transform the end variable into the position of the last index
    return begin, end

# Function to receive an image to find the bar and the second image to display the results
def findBar(image, image2):
    lines = []
    prev = [0,0]
    for i in range(len(image)):
        total = Counter(image[i])
        if total[0] > total[255]: # If find a line where there is more black pixels than white ones
            if total[0] > prev[0]: # Verification to keep only the line with more black pixels
                lines.clear()
                begin, end = findBeginEnd(list(image[i]), 0)
                lines.append([i, begin, end])
                prev[0] = total[0]
            elif total[0] == prev[0]: # If has the same quantity of black pixels, it will keep the line
                begin, end = findBeginEnd(list(image[i]), 0)
                lines.append([i, begin, end])
                prev[0] = total[0]

    # Getting the X, Y points to draw the rectangle
    firstX = lines[0][1]
    firstY = lines[0][0]
    lastX = lines[-1][2]
    lastY = lines[-1][0]

    # Rectangle to show the principal bar
    cv2.rectangle(image2, (firstX, firstY), (lastX, lastY), (0, 0, 255), 1)

    # Point in the middle of the rectangle
    middleX = int((firstX + lastX) / 2)
    middleY = int((firstY + lastY) / 2)
    cv2.circle(image2, (middleX, middleY), radius=0, color=(255, 0, 0), thickness=-1)

    # Points of each phoneme based on the width size
    print('Type the amount of phonemes in the image:')
    cv2.imshow('imagem', image2)
    cv2.waitKey()
    phonemes = int(input('Amount: '))
    width = int((lastX - firstX) / phonemes) + 2
    points = segments(width)
    result = ''
    imageX = firstX
    for _ in range(phonemes):
        outcome = ''
        for point in points:
            outcome += '1' if image[firstY + point[1]][imageX + point[0]] == 0 else '0'
            cv2.circle(image2, (imageX + point[0], firstY + point[1]), radius=1, color=(0, 255, 0), thickness=-1)
        cv2.circle(image2, (imageX, firstY), radius=1, color=(0, 255, 0), thickness=-1)
        imageX = imageX + width - 3
        result += getPhoneme(outcome) # Decoding the character
    # Scaling the image to show the outcome
    scale_percent = 400
    resized = cv2.resize(image2, (int(image2.shape[1] * scale_percent / 100),int(image2.shape[0] * scale_percent / 100)))
    cv2.imshow('imagem', resized)
    cv2.waitKey()
    return result

# Main function to treat the image and get the phoneme
def analyser(image):
    img = cv2.imread(image)
    blur = cv2.GaussianBlur(img,(5,5),5) # Applying blur 
    imgGray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY) # Applying greyscale filter
    imgThresh = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 15) # Applying threshold filter to convert greyscale into black or white
    character = findBar(imgThresh, img) # Searching the possible character
    print(character)

# Function to get each segment based on the bar width
def segments(width):
    points = []
    # Consonants
    points.append([int(width / 4),     int((-width / 4) * 1.5)]) # Segment A
    points.append([int(width / 2),     int(-width / 2)])         # Segment B
    points.append([int(width * 3 / 4), int((-width / 4) * 1.5)]) # Segment C
    points.append([int(width / 4),     int(width / 2)])          # Segment D
    points.append([int((width / 2)),   int((width / 2) * 1.3)])  # Segment E
    points.append([int(width * 3 / 4), int(width / 2)])          # Segment F
    # Vowels
    points.append([int(width * 3 / 4), int((-width / 4) * 2.3)]) # Segment 1
    points.append([int(width / 4),     int((-width / 4) * 2.3)]) # Segment 2
    points.append([int(3),             int(-width / 4)])         # Segment 3
    points.append([int((width / 4)),   int(width * 3 / 4)])      # Segment 4
    points.append([int(width * 3 / 4), int(width * 3 / 4)])      # Segment 5
    return points

# Function to decode the character
def getPhoneme(outcome):
    cons = outcome[:6] # The first 6 codes are the consonants
    vow = outcome[6:] # After the first 6 codes, there are the vowels

    # In case that doesn't find the correspondent phoneme
    cPhoneme = '?' if cons not in consonant else consonant[cons]
    vPhoneme = '?' if vow not in vowel else vowel[vow]
    return cPhoneme + vPhoneme

def main():
    analyser('./assets/tests/1.PNG')

if __name__ == '__main__':
    global vowel
    global consonant
    consonant = {}
    consonant['010001'] = 'b' # As in Baby
    consonant['100010'] = 'ch' # As in Chat
    consonant['010101'] = 'd' # As in Dog
    consonant['001110'] = 'f' # As in Fox
    consonant['001011'] = 'g' # As in Gun
    consonant['010011'] = 'h' # As in Hop
    consonant['010100'] = 'j' # As in Jam
    consonant['011001'] = 'k' # As in Kart, Cat
    consonant['010010'] = 'l' # As in  Live
    consonant['000101'] = 'm' # As in Main
    consonant['100101'] = 'n' # As in Net
    consonant['111111'] = 'ng' # As in Rink
    consonant['001010'] = 'p' # As in Pop
    consonant['011010'] = 'r' # As in Run
    consonant['011110'] = 's' # As in Sit
    consonant['101111'] = 'sh' # As in Shut
    consonant['101010'] = 't' # As in Tunic
    consonant['111010'] = 'th' # As in Thick
    consonant['010111'] = 'dh' # As in This
    consonant['110001'] = 'v' # As in Vine
    consonant['101000'] = 'w' # As in Wit
    consonant['110010'] = 'y' # As in You
    consonant['110011'] = 'z' # As in Zit
    consonant['111101'] = 'zh' # As in Azure
    consonant['000000'] = '' # If finds nothing

    vowel = {}
    vowel['11100'] = 'a' # As in Glass
    vowel['11011'] = 'ar' # As in Arm
    vowel['01100'] = 'ah' # As in Swan
    vowel['01000'] = 'ay' # As in Bay
    vowel['00111'] = 'e' # As in End
    vowel['01111'] = 'ee' # As in Bee
    vowel['01101'] = 'eer' # As in Beer
    vowel['11000'] = 'eh' # As in The
    vowel['00101'] = 'ere' # As in Air
    vowel['00011'] = 'i' # As in Bit
    vowel['10000'] = 'ie' # As in Guy
    vowel['10111'] = 'ir' # As in Bird
    vowel['11111'] = 'oh' # As in Toe
    vowel['00010'] = 'oi' # As in Toy
    vowel['11110'] = 'oo' # As in Too
    vowel['00110'] = 'ou' # As in Wolf
    vowel['00001'] = 'ow' # As in How
    vowel['11101'] = 'ore' # As in Your
    vowel['00000'] = '' # If finds nothing
    main()