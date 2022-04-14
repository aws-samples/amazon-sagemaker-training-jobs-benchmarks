## Amazon SageMaker Training jobs instance types benchmark Examples

This repository contains examples and related resources for Amazon SageMaker Training jobs over different instance types focusing on the aspects of time to train and cost to train.


## Overview

Amazon SageMaker makes it easy to train machine learning using EC2 instances. There are many instance types to choose from and this choice affects the speed and cost of training. This repository contains example benchmark for various deep learning use cases. You can see results directly in the notebook, reproduce results by re-running the notebooks. And alter the notebooks to create new scenarios to benchmark.

### Repository Structure

The repository contains the following resources:

- **G5 instance types benchmarks:**  

  - [ml.g5.2xlarge vs. ml.p3.2xlarge for training RoBERTa NLP model](instance_types_RoBERTa_benchmark) - This notebook shows how to evaluate which instance to use to train faster and chaper. It includes measures time-to-train and 

## Questions?

Raise an issue on this repo.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the Apache License 2.0 License. See the LICENSE file.
