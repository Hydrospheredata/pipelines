import kfp
import json
import os
import copy
from kfp import components
from kfp import dsl
from kfp.dsl import ContainerOp, PipelineVolume, PipelineConf, get_pipeline_conf, RUN_ID_PLACEHOLDER
from kfp.aws import use_aws_secret

cur_file_dir = os.path.dirname(__file__)
components_dir = os.path.join(cur_file_dir, '../../../../components/hydrosphere/serving/')

train_op = components.load_component_from_file('train/component.yaml')
release_op = components.load_component_from_file(components_dir + '/release_op/component.yaml')
deploy_op = components.load_component_from_file(components_dir + '/deploy_op/component.yaml')


PVC_NAME = "efs-claim"
MOUNT_PATH = "/mnt/pipeline/"
RUNTIME = "hydrosphere/serving-runtime-python-3.7:2.3.2"
INSTALL_COMMAND = "pip install -r requirements.txt"


@dsl.pipeline(
    name='Pipeline example',
    description='Hydrosphere train/release/deployment sample pipeline'
)
def pipeline(
        train_path="s3://path/to/data.csv",
        cluster="https://example-cluster.io",
        model_name="adult_kfp",
        application_name="adult_kfp",
):  
    conf: PipelineConf = get_pipeline_conf()
    conf.add_op_transformer(use_aws_secret())
    conf.set_image_pull_policy('Always')

    pvolume = PipelineVolume(pvc=PVC_NAME)

    train: ContainerOp = train_op(
        train_path=train_path,
        output_serving_path=os.path.join(MOUNT_PATH, RUN_ID_PLACEHOLDER),
    )
    train.add_pvolumes({MOUNT_PATH: pvolume})

    release: ContainerOp = release_op(
        cluster=cluster,
        model_name=model_name,
        payload=train.outputs["payload"],
        contract=train.outputs["contract"],
        path=os.path.join(MOUNT_PATH, RUN_ID_PLACEHOLDER),
        runtime=RUNTIME, 
        install_command=INSTALL_COMMAND,
    )
    release.add_pvolumes({MOUNT_PATH: pvolume})
    
    deploy = deploy_op(
        cluster=cluster, 
        application_name=application_name,
        model_name=model_name,
        model_version=release.outputs['version'],
    )


if __name__ == '__main__':
    kfp.compiler.Compiler().compile(pipeline, __file__ + '.tar.gz')
