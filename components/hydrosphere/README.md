# Hydrosphere Serving Components for Kubeflow Pipelines

## Summary

Hydrosphere Serving Components for Kubeflow Pipelines allows you to
upload your models trained on previous steps of pipelines to Hydrosphere
platform and create an applications which serves prediction requests by
HTTP or gRPC.


## Components

Hydrosphere Serving Components for Kubeflow Pipelines provides an
integration between [Hydrosphere Serving]() model serving benefits and
Kubeflow orchestration capabilities. This allows launching training jobs
as well as serving the same models in Kubernetes.

### Serving components

#### Deploy

The Deploy component allows you to upload model trained in a Kubeflow
pipelines workflow to a Hydrosphere platform.

For more information, check
[Hydrosphere Deploy Kubeflow Component](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere/serving/deploy_op)


#### Release

The Relase component allows you to create an Application from a model
previously uploaded to Hydrosphere platform. This application will be
capable of serving prediction requests by HTTP or gRPC.

For more information, check
[Hydrosphere Release Kubeflow Component](https://github.com/kubeflow/pipelines/tree/master/components/hydrosphere/serving/release_op)

