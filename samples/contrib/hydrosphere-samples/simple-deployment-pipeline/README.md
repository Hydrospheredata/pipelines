# Simple pipeline for the deployment component

An example pipeline which trains a simple classification model and deploys it to Hydrosphere. The pipeline consists of 3 components:
1. Model Training
2. [Hydrosphere Release Component](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere/serving/release_op)
   which uploads a trained model to the Hydrosphere platform
3. [Hydrosphere Deploy Component](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere/serving/deploy_op)
   which deploys an uploaded model from the last step to serve predictions


## Prerequisites

Make sure you have set up your cluster as described
[here](https://github.com/kubeflow/pipelines/blob/master/samples/contrib/hydrosphere-samples/README.md).


## Inputs to the pipeline

There are 4 main parameters user can manipulate from the Kubeflow UI:
1. `train_path` — points to the data, which should be used for training the model. It can be either an S3 path, or a local filesystem path to the training data, mounted to the training step. 
2. `cluster` — points to the Hydrosphere cluster, available for the current Kubeflow environment. 
3. `model_name` — a name of the model to be used, when uploading it to the Hydrosphere. 
4. `app_name` — a name of the application to be used, when deploying the model within Hydrosphere. 

Under the hood there are a few more constant parameters, which you *should* revise before submitting this pipeline for execution. 

The pipeline utilizes an existing PVC on the cluster to be mounted to steps. Change the value of `PVC_NAME` variable within `pipeline.py` to the existing PVC name in your cluster.

You can also adjust the values of `RUNTIME` and `INSTALL_COMMAND` variables if you need. Consult Hydrosphere [documentation](https://hydrosphere.io/serving-docs/latest/getting-started/serving-simple-model.html) for more information.

### Sample Census Income dataset

For the training dataset we chose publicly available [Census Income Data Set](https://archive.ics.uci.edu/ml/datasets/census+income). Download it to your S3 bucket, or place within mounted PVC.
