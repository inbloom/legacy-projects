#!/bin/bash

if [ -d "doc-xml_source" ]; then
    rm -rf doc-xml_source
fi
mkdir doc-xml_source
mkdir doc-xml_source/common
cp ../common/entities.ent doc-xml_source/common/
mkdir doc-xml_source/modules
cp ../modules/*.xml doc-xml_source/modules/
cp -r ../modules/concepts doc-xml_source/modules/
cp -r ../modules/reference doc-xml_source/modules/
cp -r ../modules/tasks doc-xml_source/modules/
mkdir doc-xml_source/doc-admin
cp ../doc-admin/doc-admin.xml doc-xml_source/doc-admin/
cp ../doc-admin/doc-admin-revhistory.xml doc-xml_source/doc-admin/
mkdir doc-xml_source/doc-developer
cp ../doc-developer/doc-developer.xml doc-xml_source/doc-developer/
mkdir doc-xml_source/doc-ingestion
cp ../doc-ingestion/doc-ingestion.xml doc-xml_source/doc-ingestion/
cp ../doc-ingestion/doc-ingestion-revhistory.xml doc-xml_source/doc-ingestion/
mkdir doc-xml_source/doc-runbook
cp ../doc-runbook/doc-runbook.xml doc-xml_source/doc-runbook/
cp ../doc-runbook/doc-runbook-revhistory.xml doc-xml_source/doc-runbook/
