# Hydrosphere Application Deployment Kubeflow Pipeline component

## Summary

A component to deploy a single-staged application from the existing ModelVersion on the Hydrosphere platform directly from a Kubeflow Pipelines workflow.

# Details

## Intended Use

To deploy a single-staged application without any traffic splitting from a released ModelVersion.

## Runtime Arguments
    
Argument | Description | Optional | Data type | Default |
:------- | :---------- | :------- | :-------- | :------ |
cluster | An HTTP endpoint of the Hydrosphere platform. | No | str | |
application_name | The name of the application to be deployed | No | str | |
model_name | The name of the model to be released. | No | str | |
model_version | The version of the model to be deployed | No | str | |
metadata | An additional metadata for the model. | Yes | Dict[str, str] | {} |

## Outputs

None.

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
