"""This script downloads the logs of a SageMaker training job to a local folder"""

import os
from datetime import datetime
from zipfile import ZipFile
import boto3

SAGEMAKER_STREAM_GROUP = '/aws/sagemaker/TrainingJobs'
WAITING_ANIM = ['-', '\\', '|', '/', '-', '\\', '|']

cw_client = boto3.client('logs')

def get_training_log_stream_name(training_name):
    """get the stream name of the training

    :param str training_name: the name of the training
    :return: all stream names
    : rtype: list
    """
    response = cw_client.describe_log_streams(
        logGroupName=SAGEMAKER_STREAM_GROUP,
        logStreamNamePrefix=training_name,
    )

    stream_names = [log['logStreamName'] for log in response['logStreams']]
    if len(stream_names) > 1:
        print('Found the following streams:')
        for i, s in enumerate(stream_names):
            print(f'    #{i}: {s}')

    return stream_names


def download_sagemaker_training_job_logs(job_name):
    """download the training log to local storage

    :param str training_name: the name of the training job
    """
    tmp_folder = '/tmp'
    logs_folder = f'{tmp_folder}/{job_name}'
    os.makedirs(logs_folder, exist_ok=True)
    
    streams = get_training_log_stream_name(job_name)
    for stream_name in streams:
        download_stream(tmp_folder, stream_name)
    
    # create a zip file from the logs_folder
    zip_file_name = f'{logs_folder}.zip'
    with ZipFile(zip_file_name, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(logs_folder):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.relpath(filePath, logs_folder))
    print(f'A zip file of all logs created at {zip_file_name}')


def download_stream(tmp_folder, stream):
    kw = {
            'logGroupName': SAGEMAKER_STREAM_GROUP,
            'logStreamName': stream,
            'startFromHead': True
        }

    log_path = f'{tmp_folder}/{stream}.log'
    print(f'Writing stream {stream} log to {log_path}')

    last_index = 'start'
    anim_idx = 0

        # write the log to file
    with open(log_path, 'w') as f:
        while last_index:
            res = cw_client.get_log_events(**kw)
            for event_idx, e in enumerate(res['events']):
                msg = e['message'].encode('ascii', errors='ignore').decode()
                non_ascii = msg != e['message']
                timestamp = datetime.fromtimestamp(e['timestamp']/ 1000)
                msg = f"{timestamp} {'binary-omitted' if non_ascii else ''}: {msg}"
                f.write(msg)

                    # show some animation for the user
                if event_idx % 1000 == 0:
                    print(WAITING_ANIM[anim_idx % len(WAITING_ANIM)], end="\r")
                    anim_idx += 1

            if not res['events']:
                break

            last_index = res.get('nextForwardToken')
            kw['nextToken'] = last_index
    

def read_job_name():
    """read the job name from the command line"""
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: python {sys.argv[0]} <job name or ARN>')
        sys.exit(1)
    job_name = sys.argv[1]
    if job_name.startswith('arn:'):
        job_name = job_name.split('/')[-1]
    return job_name
    

if __name__ == "__main__":
    download_sagemaker_training_job_logs(read_job_name())
