#
# Copyright 2019-Present Sonatype Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests
import sys

from yaml import dump as yaml_dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <IQ_SERVER_URL> <IQ_SERVER_VERSION>')
    sys.exit(0)

IQ_SERVER_URL = sys.argv[1]
IQ_SPEC_PATH = '/api/v2/endpoints/public'
IQ_VERSION = sys.argv[2]

json_spec_response = requests.get(f'{IQ_SERVER_URL}{IQ_SPEC_PATH}')
json_spec = json_spec_response.json()

# Add OpenAPI Info Block
if 'info' not in json_spec:
    print('Adding `info`')
    json_spec['info'] = {
        'title': 'Sonatype IQ Server',
        'description': 'This documents the available APIs into [Sonatype IQ Server]'
                       '(https://www.sonatype.com/products/open-source-security-dependency-management).',
        'contact': {
            'name': 'Sonatype Community Maintainers',
            'url': 'https://github.com/sonatype-nexus-community'
        },
        'license': {
            'name': 'Apache 2.0',
            'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
        },
        'version': IQ_VERSION
    }

# Add `securitySchemes` under `components`
if 'components' in json_spec and 'securitySchemes' not in json_spec['components']:
    print('Adding `securitySchemes`...')
    json_spec['components']['securitySchemes'] = {
        'BasicAuth': {
            'type': 'http',
            'scheme': 'basic'
        }
    }
if 'security' not in json_spec:
    json_spec['security'] = [
        {
            'BasicAuth': []
        }
    ]

# Fix Response schema for GET /api/v2/applications
if 'paths' in json_spec and '/api/v2/applications' in json_spec['paths']:
    if 'get' in json_spec['paths']['/api/v2/applications']:
        print('Fixing GET /api/v2/application...')
        json_spec['paths']['/api/v2/applications']['get']['responses'] = {
            'default': {
                'description': 'default response',
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'array',
                            'items': {
                                '$ref': '#/components/schemas/ApiApplicationCategoryDTO'
                            }
                        }
                    }
                }
            }
        }

# Fix `ApiComponentDetailsDTOV2` schema
if 'components' in json_spec and 'schemas' in json_spec['components'] \
        and 'ApiComponentDetailsDTOV2' in json_spec['components']['schemas']:
    print('Fixing schema: ApiComponentDetailsDTOV2...')
    new_api_component_details_dto_v2 = json_spec['components']['schemas']['ApiComponentDetailsDTOV2']

    new_api_component_details_dto_v2['properties']['hygieneRating'].update({'nullable': True})
    new_api_component_details_dto_v2['properties']['integrityRating'].update({'nullable': True})
    new_api_component_details_dto_v2['properties']['relativePopularity'].update({'nullable': True})

    json_spec['components']['schemas']['ApiComponentDetailsDTOV2'] = new_api_component_details_dto_v2

# Remove APIs with incomplete schemas
API_PATHS_TO_REMOVE = {
    '/api/v2/licenseLegalMetadata/customMultiApplication/report': [],
    '/api/v2/product/license': [],
    '/api/v2/config/saml': ['put']
}
if 'paths' in json_spec:
    print('Removing paths...')
    for path, methods in API_PATHS_TO_REMOVE.items():
        print(f'   Removing: {path} : {methods}')
        if path in json_spec['paths']:
            if len(methods) == 0:
                json_spec['paths'].pop(path)
            else:
                for method in methods:
                    json_spec['paths'][path].pop(method)

with open('./spec/openapi.yaml', 'w') as output_yaml_specfile:
    output_yaml_specfile.write(yaml_dump(json_spec))
