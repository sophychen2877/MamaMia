import base64
import json

from google.cloud import storage
from google.cloud import vision


vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()




with open('config.json') as f:
    data = f.read()
config = json.loads(data)

# [START functions_ocr_detect]
def detect_text(bucket, vision_filename):
    print('Looking for text in image {}'.format(filename))

    text_detection_response = vision_client.text_detection({
        'source': {'image_uri': 'gs://{}/{}'.format(bucket, filename)}
    })

    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description

    else:
        text = ''
    #print('Extracted text {} from image ({} chars).'.format(text, len(text)))
    return text

# [END functions_ocr_detect]


# [START message_validatation_helper]
def validate_message(message, param):
    var = message.get(param)
    if not var:
        raise ValueError('{} is not provided. Make sure you have \
                          property {} in the request'.format(param, param))
    return var
# [END message_validatation_helper]


# [START functions_ocr_save]
def save_result(event, context):

    message_data = base64.b64decode(event['data']).decode('utf-8')
    message = json.loads(message_data)


    text = validate_message(message, 'text')
    filename = validate_message(message, 'filename')

    print('Received request to save file {}.'.format(filename))

    bucket_name = config['RESULT_BUCKET']
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    print('Saving result to {} in bucket {}.'.format(filename,
                                                     bucket_name))

    blob.upload_from_string(text)

    print('File saved.')
# [END functions_ocr_save]

def set_event(text_filename, text):
    data = base64.b64encode(json.dumps({
        'text': text,
        'filename': text_filename,
        'lang': 'en',
    }).encode('utf-8'))
    event = {
        'data': data
    }
    return event




if __name__ == '__main__':

    bucket = 'fr-receipts'
    vision_filename = input('which receipt in the bucket would you like to scan:')
    #vision_filename = 'another-walmart-receipt2.png'
    context = {}
    text_filename = input('what name would you like to name your text file as:')


    text = detect_text(bucket, vision_filename)
    event = set_event(text_filename, text)
    save_result(event, context)
