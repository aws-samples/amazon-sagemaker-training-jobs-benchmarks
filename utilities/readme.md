# SageMaker Training Utilities
 - [fit_with_retries.py](fit_with_retries.py) - helps overcome temporary errors, like insufficient capacity error, when launching a SageMaker Training job.
 - [download_sagemaker_job_logs.py](download_sagemaker_job_logs.py) - Downloads the logs of a SageMaker training job to a local folder (supports distributed training). Useful when you prefer viewing and analyzing logs locally instead of via CloudWatch, or you need to provide your logs to AWS support, as part of a case.
