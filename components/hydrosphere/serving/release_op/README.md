# Hydrosphere Model Release Kubeflow Pipeline component

## Summary

A component to release a new ModelVersion to the Hydrosphere platform directly from a Kubeflow Pipelines workflow.

# Details

## Intended Use

To upload a new ModelVersion to the Hydrosphere platform after a model has been trained.

## Runtime Arguments
    
Argument | Description | Optional | Data type | Default |
:------- | :---------- | :------- | :-------- | :------ |
cluster | An HTTP endpoint of the Hydrosphere platform. | No | str | |
model_name | The name of the model to be released. | No | str | |
path | A path to the model's root folder, where all model artifacts are stored. Not required for external models. | Yes | str | '' |
payload | A payload of the model, listing all the artifacts to be uploaded in the root folder. Not required for external models. | Yes | List[str] | [] | 
contract_path | A path to the contract of the model, describing model's inputs and outputs. | No | str | |
runtime | A runtime for the model to be used when serving predictions. Not required for external models. | Yes | str | '' |
install_command | An install command to be executed on the model build phase. Sets up a runtime environment. | Yes | str | '' |
training_data | A path to the training data (CSV only) to be uploaded during model release. Should be either a local path or an S3 path. | Yes | str | '' |
metadata | An additional metadata for the model. | Yes | Dict[str, str] | {} |

Notes:
* Payload and contract paths should be available locally for the step, e.g., mounted as a volume and submitted as parameters. 
* Contract should resemble the structure of the [contract object](https://hydrosphere.io/serving-docs/latest/how-to/write-definitions.html#contract-object).  
* Training path could be either a path to the local csv file (e.g., mounted as a volume), or an S3 URI.

## Outputs

Name | Description |
:--- | :---------- |
version | A version of the model release under the provided name. |

# Requirements
* [Kubeflow pipelines SDK](https://www.kubeflow.org/docs/pipelines/sdk/install-sdk/)
* [Kubeflow set-up](https://www.kubeflow.org/docs/aws/deploy/install-kubeflow/)

# Samples
## On its own
K-Means algorithm tuning on MNIST dataset: [pipeline](https://github.com/kubeflow/pipelines/blob/master/samples/contrib/aws-samples/mnist-kmeans-sagemaker/kmeans-hpo-pipeline.py)

Follow the steps as in the [README](https://github.com/kubeflow/pipelines/blob/master/samples/contrib/aws-samples/mnist-kmeans-sagemaker/README.md) with some modification:
1. Get and store data in S3 buckets
2. Prepare an IAM roles with permissions to run SageMaker jobs
3. Add 'aws-secret' to your kubeflow namespace
4. Compile the pipeline:
```bash
dsl-compile --py kmeans-hpo-pipeline.py --output kmeans-hpo-pipeline.tar.gz
```
5. In the Kubeflow UI, upload the compiled pipeline specification (the .tar.gz file) and create a new run. Update the role_arn and the data paths, and optionally any other run parameters.
6. Once the pipeline completes, you can see the outputs under 'Output parameters' in the HPO component's Input/Output section.

## Integrated into a pipeline
MNIST Classification using K-Means pipeline: [Pipeline](https://github.com/kubeflow/pipelines/blob/master/samples/contrib/aws-samples/mnist-kmeans-sagemaker/mnist-classification-pipeline.py) | [Steps](https://github.com/kubeflow/pipelines/blob/master/samples/contrib/aws-samples/mnist-kmeans-sagemaker/README.md)

# Resources
* [Using Amazon built-in algorithms](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html)
* [More information on request parameters](https://github.com/awsdocs/amazon-sagemaker-developer-guide/blob/master/doc_source/API_CreateHyperParameterTuningJob.md#request-parameters)
