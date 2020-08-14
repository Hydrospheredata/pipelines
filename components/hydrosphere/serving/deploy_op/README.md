# Hydrosphere Application Deployment Kubeflow Pipeline component

## Summary

A component to deploy a single-staged application from the existing
ModelVersion on the Hydrosphere platform directly from a Kubeflow
Pipelines workflow.

# Details

## Intended Use

To deploy a single-staged application without any traffic splitting from
a released ModelVersion.

## Runtime Arguments

| Argument         | Description                                    | Optional | Data type        | Default |
|:-----------------|:-----------------------------------------------|:---------|:-----------------|:--------|
| cluster          | An HTTP endpoint of the Hydrosphere platform.  | No       | str              |         |
| application_name | The name of the application to be deployed.    | No       | str              |         |
| model_name       | The name of the model uploaded to Hydrosphere. | No       | str              |         |
| model_version    | The version of the model to be deployed.       | No       | str              |         |
| metadata         | An additional metadata for the application.    | Yes      | Dict\[str, str\] | {}      |

## Outputs

None.

# Requirements

* [Kubeflow pipelines SDK](https://www.kubeflow.org/docs/pipelines/sdk/install-sdk/)
* [Hydrosphere Python SDK](https://hydrospheredata.github.io/hydro-serving-sdk/quickstart.html#installation)
* [Kubeflow set-up](https://www.kubeflow.org/docs/aws/deploy/install-kubeflow/)
* [Hydrosphere set-up](https://hydrosphere.io/serving-docs/latest/install/index.html)

# Samples

## On its own

TODO

## Integrated into a pipeline

TODO

# Resources

