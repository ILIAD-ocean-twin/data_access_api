# Application description

Queryables
* spatial validity - bbox
* dct:title
* dct:description - free text comes from cwl
* dct:publisher - string


Non-queryables
* id - URI
* licence - SPDX Identifier https://spdx.org/licenses/ of the service
* link to the CWL/OGC API Process - separate records for these two
* other links including cross-links between CWL and API Processes

Excluded after discussion and will be not used:
* time validity
* formats - considered as list of mime types, decided it is included in the cwl
