# Sample Hydrosphere Kubeflow Pipelines

This folder contains example pipelines which use
[Hydrosphere Components for KFP](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere).


The following sections explain the setup needed to run these pipelines.
Once you are done with the setup,
[simple-deployment-pipeline](https://github.com/kubeflow/pipelines/tree/master/samples/contrib/hydrosphere-samples/simple-deployment-pipeline)
is a good place to start if you have never used these components before.

Read more about Hydrosphere
[here](https://github.com/Hydrospheredata/hydro-serving).

## Prerequisites

1. You need a cluster with Kubeflow installed on it.
   Follow [this](https://www.kubeflow.org/docs/started/getting-started/) instructions to set up a Kubeflow instance.
2. You need a cluster with Hydrosphere installed on it.
   Follow [this](https://hydrosphere.io/serving-docs/latest/install/index.html) instructions to set up a Hydrosphere instance. 
3. Install the following on your local machine
   1. [Kubeflow Pipelines SDK](https://www.kubeflow.org/docs/pipelines/sdk/install-sdk/#install-the-kubeflow-pipelines-sdk)

## Pipelines

1. [Simple deployment pipeline](simple-deployment-pipeline/) - train a simple model and deploy it to Hydrosphere.