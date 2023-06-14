<!--

    Copyright 2019-Present Sonatype Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

-->

# Nexus IQ Server API Client(s)

[![CircleCI](https://circleci.com/gh/sonatype-nexus-community/nexus-iq-api-client/tree/main.svg?style=svg)](https://circleci.com/gh/sonatype-nexus-community/nexus-iq-api-client/tree/main)
[![GitHub license](https://img.shields.io/github/license/sonatype-nexus-community/nexus-iq-api-client)](https://github.com/sonatype-nexus-community/nexus-iq-api-client/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/sonatype-nexus-community/nexus-iq-api-client)](https://github.com/sonatype-nexus-community/nexus-iq-api-client/issues)
[![GitHub forks](https://img.shields.io/github/forks/sonatype-nexus-community/nexus-iq-api-client)](https://github.com/sonatype-nexus-community/nexus-iq-api-client/network)
[![GitHub stars](https://img.shields.io/github/stars/sonatype-nexus-community/nexus-iq-api-client)](https://github.com/sonatype-nexus-community/nexus-iq-api-client/stargazers)

----

This repository produces generated API Clients in various languages and frameworks for use by Customers and other projects.

## Supported Languages & Frameworks

| Language / Framework | Nexus IQ Version Added | Public Package Link |
| -------------------- | ---------------------- | ------------------- |
| Typescript (fetch)   | 156 | [NPM](https://www.npmjs.com/package/@sonatype/nexus-iq-api-client) |

## Known Issues

### APIs Excluded from Generation

The following API endpoints are removed from the schema prior to generation of the API Client libraries.

| API Endpoint | Method | Reason |
| ------------ | ------ | ------ |
| /api/v2/licenseLegalMetadata/customMultiApplication/report | POST | Relies on a schema of undefined `object` - generated code is invalid in Typescript. |
| /api/v2/product/license | POST | Relies on a schema of undefined `object` - generated code is invalid in Typescript. |
| /api/v2/product/license | DELETE | Relies on a schema of undefined `object` - generated code is invalid in Typescript. |
| /api/v2/config/saml | PUT | Relies on a schema of undefined `object` - generated code is invalid in Typescript. |

### Additional Changes to OpenAPI Schema prior to Generation

1. Authentication is not defined - add the YAML block under `components`:
   ```
   ...
      securitySchemes:
        BasicAuth:
            type: http
            scheme: basic
   ...
   ```
  And add the root `security` block to the end of the schema file:
  ```
  ...
  security:
    - BasicAuth: []
  ```

2. Response Schema added to `getApplications`:
   ```
        application/json:
              schema:
                type: object
                properties:
                  applications:
                    type: array
                    items:
                      $ref: '#/components/schemas/ApiApplicationDTO'
   ```


## Getting the latest OpenAPI Schema

Get it from your Sonatype IQ Server at `/api/v2/endpoints/public`.

## Generation of API Clients

```
docker run --rm -v "$(PWD):/local" openapitools/openapi-generator-cli batch --clean /local/typescript.yaml

docker run --rm -v "$(PWD):/local" openapitools/openapi-generator-cli generate -i /local/spec/openapi.yaml -g typescript-fetch -o /local/out/test -c /local/openapi-config.yaml -v > out.log
```

## Changelog

See our [Change Log](./CHANGELOG.md).

## Releasing

We use [semantic-release](https://python-semantic-release.readthedocs.io/en/latest/) to generate releases
from commits to the `main` branch.

We aim to keep the MINOR version component in-line with the version of Nexus IQ Server for which the API Client is generated - i.e. `1.156.x` are all releases generated for the API specification as shipped with Nexus IQ Server version 156.

For example, to perform a "patch" release, add a commit to `main` with a comment like below. The `fix: ` prefix matters.

```
fix: the problem resolved goes here
```

## The Fine Print

Remember:

It is worth noting that this is **NOT SUPPORTED** by Sonatype, and is a contribution of ours to the open source
community (read: you!)

* Use this contribution at the risk tolerance that you have
* Do NOT file Sonatype support tickets related to `nexus-iq-api-client`
* DO file issues here on GitHub, so that the community can pitch in

Phew, that was easier than I thought. Last but not least of all - have fun!
