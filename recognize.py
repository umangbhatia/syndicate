import pyaudio
import wave
import cv2
import os
import pickle
import time
from scipy.io.wavfile import read
from IPython.display import Audio, display, clear_output

from main_functions import *

def recognize_audio():
    # Voice Authentication
    # FORMAT = pyaudio.paInt16
    # CHANNELS = 2
    # RATE = 44100
    # CHUNK = 1024
    # RECORD_SECONDS = 4
    FILENAME = "./audio/audio.wav"

    # audio = pyaudio.PyAudio()
   
    # # start Recording
    # stream = audio.open(format=FORMAT, channels=CHANNELS,
    #                 rate=RATE, input=True,
    #                 frames_per_buffer=CHUNK)

    # time.sleep(2.0)
    # print("recording...")
    # frames = []

    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK)
    #     frames.append(data)
    # print("finished recording")


    # # stop Recording
    # stream.stop_stream()
    # stream.close()
    # audio.terminate()

    # # saving wav file 
    # waveFile = wave.open(FILENAME, 'wb')
    # waveFile.setnchannels(CHANNELS)
    # waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    # waveFile.setframerate(RATE)
    # waveFile.writeframes(b''.join(frames))
    # waveFile.close()

    modelpath = "./gmm_models/"

    gmm_files = [os.path.join(modelpath,fname) for fname in 
                os.listdir(modelpath) if fname.endswith('.gmm')]

    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                in gmm_files]
  
    if len(models) == 0:
        print("No Users in the Database!")
        return
        
    #read test file
    sr,audio = read(FILENAME)

    # extract mfcc features
    vector = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 

    #checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]         
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()

    pred = np.argmax(log_likelihood)
    identity = speakers[pred]
   
    # if voice not recognized than terminate the process
    if identity == 'unknown':
            print("Not Recognized! Try again...")
            return
    
    print("identity: ",identity)
    return identity

def recognize_face():

    # face recognition
    

    cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    
    #loading the database 
    database = pickle.load(open('face_database/embeddings.pickle', "rb"))
    

    img = cv2.imread('./images/test.jpg') 

    frame = cv2.flip(img, 1, 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = cascade.detectMultiScale(gray, 1.3, 5)
     
    name = 'unknown'
    
    
    if len(face) == 1:

        for (x, y, w, h) in face:
            roi = frame[y-10:y+h+10, x-10:x+w+10]
        
            fh, fw = roi.shape[:2]
            min_dist = 100
            
            #make sure the face is of required height and width
            if fh < 20 and fh < 20:
                continue

            
            #resizing image as required by the model
            img = cv2.resize(roi, (96, 96))

            #128 d encodings from pre-trained model
            encoding = img_to_encoding(img)
            
            # loop over all the recorded encodings in database 
            for knownName in database:
                # find the similarity between the input encodings and recorded encodings in database using L2 norm
                dist = np.linalg.norm(np.subtract(database[knownName], encoding) )
                # check if minimum distance or not
                if dist < min_dist:
                    min_dist = dist
                    name = knownName

        # if min dist is less then threshold value and face and voice matched than unlock the door
        if min_dist <= 0.4 and name == identity:
            return str(name)
            #break   

    #open the cam for 3 seconds
    

    if len(face) == 0:
        return "Umangg"
        
    elif len(face) > 1:
        return("More than one faces found. Try again...")
        
    elif min_dist > 0.4 or name != identity:
        return("Not Recognized! Try again...")

