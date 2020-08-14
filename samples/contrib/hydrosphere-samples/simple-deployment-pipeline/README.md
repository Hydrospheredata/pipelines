# Simple pipeline for the deployment component

An example pipeline contains 3 components:
1. Model Training
2. [Hydrosphere Release Component](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere/serving/release_op)
   which uploads a trained model to the Hydrosphere platform
3. [Hydrosphere Deploy Component](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere/serving/deploy_op)
   which deploys an uploaded model from the last step to serve
   predictions


## Prerequisites

Make sure you have set up your cluster as described in this
[README.md](https://github.com/kubeflow/pipelines/blob/master/samples/contrib/hydrosphere-samples/README.md).

TODO data download?

## Steps

TODO



