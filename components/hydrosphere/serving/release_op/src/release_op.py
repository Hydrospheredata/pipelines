# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse
import logging

from hydrosdk.cluster import Cluster
from hydrosdk.modelversion import LocalModel
from hydrosdk.contract import signature_dict_to_ModelContract
from hydrosdk.exceptions import BadResponse

from common import _utils


def create_parser():
    parser = argparse.ArgumentParser(description='Hydrosphere Model Release Component')
    
    # inputs
    parser.add_argument('--cluster', type=str, required=True, help='An HTTP endpoint of the Hydrosphere platform.')
    parser.add_argument('--model_name', type=str, required=True, help='The name of the model to be released.')    
    parser.add_argument('--path', type=str, required=False, help='A path to the model root folder, where all model artifacts are stored. Not required for external models.')
    parser.add_argument('--payload', type=_utils.yaml_or_json_str, required=False, help='A payload of the model, listing all the artifacts to be uploaded in the root folder. Not required for external models.')
    parser.add_argument('--contract_path', type=str, required=True, help='A path to the contract of the model describing model\'s inputs and outputs.')
    parser.add_argument('--runtime', type=str, required=False, help='A runtime for the model to be used when serving predictions. Not required for external models.')
    parser.add_argument('--install_command', type=str, required=False, help='An install command to be executed on the model build phase.')
    parser.add_argument('--training_data', type=str, required=False, help='A path to the training data to be uploaded during model release. Should be either local path or S3 path.')
    parser.add_argument('--metadata', type=_utils.yaml_or_json_str, required=False, help='An additional metadata for the model.')

    # outputs
    parser.add_argument('--version_path', type=str, default='/tmp/version', help='A version of the model release under provided name.')
    return parser


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)

    logging.getLogger().setLevel(logging.INFO)
    cluster = Cluster(http_address=args.cluster)
    with open(args.contract_path, "r") as file:
        signature = _utils.yaml_or_json_str(file.read())
    contract = signature_dict_to_ModelContract(args.model_name, signature)
    runtime = _utils.str_to_DockerImage(args.runtime)
    training_data = args.training_data if args.training_data != '' else None
    localmodel = LocalModel(
        args.model_name, runtime, args.path, args.payload, contract, 
        args.metadata, args.install_command, training_data
    )

    logging.info("Uploading a new modelversion to Hydrosphere.")
    modelversion = localmodel.upload(cluster)
    if training_data is not None:
        logging.info("Uploading training data for the model.")
        try: 
            modelversion.upload_training_data()
            logging.info("Training data has been submitted for processing.")
        except BadResponse as e:
            logging.error(f"Failed to upload training data: {e}")
    logging.info("Waiting till the model gets released...")
    modelversion.lock_till_released()
    logging.info("The modelversion has been released.")
    
    _utils.write_output(args.version_path, str(modelversion.version))


if __name__== "__main__":
  main(sys.argv[1:])
