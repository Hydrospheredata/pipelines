# Hydrosphere Model Release Kubeflow Pipeline component

## Summary

A component to release a new ModelVersion to the Hydrosphere platform
directly from a Kubeflow Pipelines workflow.

# Details

## Intended Use

To upload a new ModelVersion to the Hydrosphere platform after a model
has been trained.

## Runtime Arguments

| Argument        | Description                                                                                                              | Optional | Data type      | Default |
|:----------------|:-------------------------------------------------------------------------------------------------------------------------|:---------|:---------------|:--------|
| cluster         | An HTTP endpoint of the Hydrosphere platform.                                                                            | No       | str            |         |
| model_name      | The name of the model to be released.                                                                                    | No       | str            |         |
| path            | A path to the model's root folder, where all model artifacts are stored. Not required for external models.               | Yes      | str            | ''      |
| payload         | A payload of the model, listing all the artifacts to be uploaded in the root folder. Not required for external models.   | Yes      | List[str]      | []      |
| contract_path   | A path to the contract of the model, describing model's inputs and outputs.                                              | No       | str            |         |
| runtime         | A runtime for the model to be used when serving predictions. Not required for external models.                           | Yes      | str            | ''      |
| install_command | An install command to be executed on the model build phase. Sets up a runtime environment.                               | Yes      | str            | ''      |
| training_data   | A path to the training data (CSV only) to be uploaded during model release. Should be either a local path or an S3 path. | Yes      | str            | ''      |
| metadata        | An additional metadata for the model.                                                                                    | Yes      | Dict[str, str] | {}      |

Notes:
* Payload and contract paths should be available locally for the step,
  e.g., mounted as a volume and submitted as parameters.
* Contract should resemble the structure of the
  [contract object](https://hydrosphere.io/serving-docs/latest/how-to/write-definitions.html#contract-object).
* Training path could be either a path to the local csv file (e.g.,
  mounted as a volume), or an S3 URI.

## Outputs

| Name    | Description                                              |
|:--------|:---------------------------------------------------------|
| version | A version of the model released under the provided name. |

# Requirements

* [Kubeflow pipelines SDK](https://www.kubeflow.org/docs/pipelines/sdk/install-sdk/)
* [Hydrosphere Python SDK](https://hydrospheredata.github.io/hydro-serving-sdk/quickstart.html#installation)
* [Kubeflow set-up](https://www.kubeflow.org/docs/started/getting-started/)
* [Hydrosphere set-up](https://hydrosphere.io/serving-docs/latest/install/index.html)

# Samples

[All Samples](https://github.com/kubeflow/pipelines/tree/master/samples/contrib/hydrosphere-samples/):

* [Simple Deployment Pipeline](https://github.com/kubeflow/pipelines/tree/master/samples/contrib/hydrosphere-samples/simple-deployment-pipeline)

# Resources

[Hydrosphere Github Repo](https://github.com/Hydrospheredata/hydro-serving)
