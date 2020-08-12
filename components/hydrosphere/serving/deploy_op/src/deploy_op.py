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
from hydrosdk.application import ApplicationBuilder, ExecutionStageBuilder
from hydrosdk.modelversion import ModelVersion

from common import _utils


def create_parser():
    parser = argparse.ArgumentParser(description='Hydrosphere Application Deployment Component')

    # inputs
    parser.add_argument('--cluster', type=str, required=True, help='An HTTP endpoint of the Hydrosphere platform.')
    parser.add_argument('--application_name', type=str, required=True, help='The name of the application to be deployed.')
    parser.add_argument('--model_name', type=str, required=True, help='The name of the model to be deployed.')
    parser.add_argument('--model_version', type=str, required=True, help='The version of the model to be deployed.')
    parser.add_argument('--metadata', type=_utils.yaml_or_json_str, required=False, help='An additional metadata for the application.')

    return parser


def main(argv=None):
    parser = create_parser()
    args = parser.parse_args(argv)

    logging.getLogger().setLevel(logging.INFO)
    cluster = Cluster(args.cluster)
    logging.info("Fetching a modelversion...")
    modelversion = ModelVersion.find(cluster, args.model_name, args.model_version)
    stage = ExecutionStageBuilder().with_model_variant(modelversion, 100).build()
    logging.info("Deploying a new application...")
    application = ApplicationBuilder(cluster, args.application_name) \
        .with_stage(stage).with_metadatas(args.metadata).build()
    logging.info("The application has been submitted for deployment.")
    

if __name__== "__main__":
  main(sys.argv[1:])
